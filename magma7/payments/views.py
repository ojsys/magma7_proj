import json
import secrets
import requests
from urllib import parse as urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from memberships.models import Plan, Subscription
from decimal import Decimal
from notifications.utils import notify_user
from .models import Payment
from .utils import send_payment_receipt


def _make_reference(prefix: str = "M7"):
    return f"{prefix}_{secrets.token_hex(8)}"


def _post_json(url: str, payload: dict, headers: dict) -> dict:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


@login_required
def initiate_payment(request, plan_id: int):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    if not getattr(settings, 'PAYMENTS_ENABLED', False):
        # Payments are disabled; do not auto-activate. Inform user and return to plans.
        messages.error(request, 'Payments are currently disabled. Please contact support to complete your subscription.')
        return redirect('memberships:plans')

    provider = getattr(settings, 'PAYMENT_PROVIDER', 'paystack')
    currency = getattr(settings, 'CURRENCY', 'NGN')

    # Amount conversion to minor units
    amount_minor = int(Decimal(str(plan.price)) * 100)
    reference = _make_reference('M7')
    payment = Payment.objects.create(
        user=request.user,
        plan=plan,
        amount=amount_minor,
        currency=currency,
        provider=provider,
        reference=reference,
    )

    if provider == 'paystack':
        secret = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
        if not secret:
            messages.error(request, 'Payment gateway not configured.')
            payment.mark_failed({'error': 'Missing PAYSTACK_SECRET_KEY'})
            return redirect('memberships:plans')
        init_url = 'https://api.paystack.co/transaction/initialize'
        callback_url = settings.SITE_URL + reverse('payments:paystack_callback')
        payload = {
            'email': request.user.email or 'placeholder@example.com',
            'amount': amount_minor,
            'currency': currency,
            'reference': reference,
            'callback_url': callback_url,
            'metadata': {'plan_id': plan.id, 'user_id': request.user.id},
        }
        headers = {
            'Authorization': f'Bearer {secret}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        try:
            resp = _post_json(init_url, payload, headers)
        except Exception as e:
            payment.mark_failed({'exception': str(e)})
            messages.error(request, f'Could not connect to Paystack: {str(e)}')
            return redirect('memberships:plans')
        if resp.get('status') and resp.get('data', {}).get('authorization_url'):
            auth_url = resp['data']['authorization_url']
            return redirect(auth_url)
        payment.mark_failed(resp)
        messages.error(request, 'Payment initialization failed.')
        return redirect('memberships:plans')

    elif provider == 'stripe':
        try:
            import stripe
        except Exception:
            messages.error(request, 'Stripe library not installed.')
            payment.mark_failed({'error': 'stripe_not_installed'})
            return redirect('memberships:plans')
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        if not stripe.api_key:
            messages.error(request, 'Stripe not configured.')
            payment.mark_failed({'error': 'missing_stripe_secret'})
            return redirect('memberships:plans')
        success_url = settings.SITE_URL + reverse('payments:stripe_success') + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = settings.SITE_URL + reverse('payments:stripe_cancel')
        try:
            session = stripe.checkout.Session.create(
                mode='payment',
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'product_data': {'name': f"{plan.name} Membership"},
                        'unit_amount': amount_minor,
                    },
                    'quantity': 1,
                }],
                metadata={'reference': reference, 'plan_id': plan.id, 'user_id': request.user.id},
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=reference,
            )
        except Exception as e:
            payment.mark_failed({'exception': str(e)})
            messages.error(request, 'Stripe session creation failed.')
            return redirect('memberships:plans')
        return redirect(session.url)

    else:
        messages.error(request, 'Unsupported payment provider.')
        payment.mark_failed({'error': 'unsupported_provider'})
        return redirect('memberships:plans')


@login_required
def paystack_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return HttpResponseBadRequest('Missing reference')
    payment = get_object_or_404(Payment, reference=reference, provider='paystack', user=request.user)
    verify_url = f'https://api.paystack.co/transaction/verify/{urlparse.quote(reference)}'
    headers = {'Authorization': f'Bearer {getattr(settings, "PAYSTACK_SECRET_KEY", "")}', 'Accept': 'application/json'}
    try:
        resp = requests.get(verify_url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        messages.error(request, 'Could not verify Paystack transaction.')
        payment.mark_failed({'exception': str(e)})
        return redirect('memberships:plans')
    if data.get('status') and data.get('data', {}).get('status') == 'success':
        payment.mark_success(data)
        # On success, create subscription and link payment
        sub = Subscription.objects.create(user=request.user, plan=payment.plan, payment=payment)
        messages.success(request, f'Payment successful. Subscription active until {sub.end_date}.')
        notify_user(request.user, title='Payment Successful', body=f'Your payment for {payment.plan.name} was successful. Your membership is now active!')

        # Send payment receipt via email
        send_payment_receipt(payment, subscription=sub)

        return redirect('memberships:dashboard')
    else:
        payment.mark_failed(data)
        messages.error(request, 'Payment failed or cancelled.')
        return redirect('memberships:plans')


@login_required
def stripe_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return HttpResponseBadRequest('Missing session_id')
    try:
        import stripe
    except Exception:
        messages.error(request, 'Stripe not available.')
        return redirect('memberships:plans')
    stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        messages.error(request, 'Unable to verify Stripe session.')
        return redirect('memberships:plans')
    reference = session.get('client_reference_id')
    payment = get_object_or_404(Payment, reference=reference, provider='stripe', user=request.user)
    if session.get('payment_status') == 'paid':
        if payment.status != 'successful':
            payment.mark_success({'session': session.id})
            sub = Subscription.objects.create(user=request.user, plan=payment.plan, payment=payment)
            messages.success(request, f'Payment successful. Subscription active until {sub.end_date}.')
            notify_user(request.user, title='Payment Successful', body=f'Your payment for {payment.plan.name} was successful. Your membership is now active!')

            # Send payment receipt via email
            send_payment_receipt(payment, subscription=sub)
        else:
            messages.success(request, 'Payment already confirmed.')
        return redirect('memberships:dashboard')
    else:
        payment.mark_failed({'session': session.id, 'payment_status': session.get('payment_status')})
        messages.error(request, 'Payment not completed.')
        return redirect('memberships:plans')


@login_required
def stripe_cancel(request):
    messages.info(request, 'Payment cancelled.')
    return redirect('memberships:plans')


def stripe_webhook(request):
    try:
        import stripe
    except Exception:
        return HttpResponseBadRequest('Stripe not available')
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=webhook_secret)
        else:
            event = json.loads(payload.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid payload or signature')

    event_type = event['type'] if isinstance(event, dict) else event.type
    data = event['data']['object'] if isinstance(event, dict) else event.data.object

    if event_type == 'checkout.session.completed':
        reference = data.get('client_reference_id') or (data.get('metadata') or {}).get('reference')
        if reference:
            try:
                payment = Payment.objects.select_related('plan', 'user').get(reference=reference, provider='stripe')
            except Payment.DoesNotExist:
                payment = None
            if payment and payment.status != 'successful':
                payment.mark_success({'webhook': True, 'session': data.get('id')})
                sub = Subscription.objects.create(user=payment.user, plan=payment.plan, payment=payment)
                notify_user(payment.user, title='Payment Successful', body=f'Your payment for {payment.plan.name} was successful. Your membership is now active!')

                # Send payment receipt via email
                send_payment_receipt(payment, subscription=sub)

    # Return a 200 so Stripe considers the webhook delivered
    from django.http import HttpResponse
    return HttpResponse(status=200)
