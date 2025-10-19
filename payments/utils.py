"""
Utility functions for payments app
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decimal import Decimal


def get_currency_symbol(currency_code: str = 'NGN') -> str:
    """
    Get currency symbol from currency code
    """
    symbols = {
        'NGN': '₦',
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'ZAR': 'R',
        'KES': 'KSh',
        'GHS': '₵',
    }
    return symbols.get(currency_code.upper(), currency_code)


def send_payment_receipt(payment, subscription=None):
    """
    Send a payment receipt email to the user

    Args:
        payment: Payment object
        subscription: Subscription object (optional)

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not payment.user.email:
        return False

    # Calculate display amount (convert from minor units back to major)
    amount_display = Decimal(payment.amount) / 100

    # Get currency symbol
    currency_symbol = get_currency_symbol(payment.currency)

    # Prepare context for email template
    context = {
        'user': payment.user,
        'payment': payment,
        'subscription': subscription,
        'site_name': getattr(settings, 'SITE_NAME', 'Magma7Fitness'),
        'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
        'currency_symbol': currency_symbol,
        'amount_display': amount_display,
    }

    # Render HTML email
    html_content = render_to_string('payments/emails/receipt.html', context)

    # Create plain text version (fallback)
    text_content = f"""
Payment Receipt - {context['site_name']}
{'=' * 50}

Thank you for your payment, {payment.user.get_full_name() or payment.user.username}!

PAYMENT SUCCESSFUL
------------------
Total Paid: {currency_symbol}{amount_display}

Transaction Details:
- Reference: {payment.reference}
- Date: {payment.updated_at.strftime('%B %d, %Y - %I:%M %p')}
- Payment Method: {payment.provider.title()}
- Status: {payment.status.title()}

Membership Plan:
- Plan: {payment.plan.name}
- Duration: {payment.plan.duration_days} days
{'- Active Until: ' + subscription.end_date.strftime("%B %d, %Y") if subscription else ''}

What's Next?
Your membership is now active! Log in to your dashboard to access all premium features.

Dashboard: {context['site_url']}/memberships/dashboard/

Need Help?
Contact us at support@magma7fitness.com or call +234 (0) 123 456 789

{context['site_name']}
No. 30 Zakaria Maimalari Street, Nasfat Layout, Kaduna

This is an automated receipt. Please keep it for your records.
    """.strip()

    # Prepare email
    subject = f'Payment Receipt - {payment.plan.name} Membership'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@magma7fitness.com')
    to_email = [payment.user.email]

    # Create email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_email,
    )

    # Attach HTML version
    email.attach_alternative(html_content, "text/html")

    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Failed to send receipt email: {str(e)}")
        return False
