"""
Management command to test the payment receipt email
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from payments.models import Payment
from payments.utils import send_payment_receipt

User = get_user_model()


class Command(BaseCommand):
    help = 'Test sending a payment receipt email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send the test receipt to',
        )

    def handle(self, *args, **options):
        email = options.get('email')

        if not email:
            # Try to find a user with an email
            user = User.objects.filter(email__isnull=False).exclude(email='').first()
            if not user:
                self.stdout.write(self.style.ERROR('No users with email found. Please create a user with an email address or specify --email'))
                return
            email = user.email
        else:
            # Find or create user with this email
            user = User.objects.filter(email=email).first()
            if not user:
                self.stdout.write(self.style.ERROR(f'No user found with email {email}'))
                return

        # Find the most recent successful payment for this user
        payment = Payment.objects.filter(
            user=user,
            status='successful'
        ).select_related('plan').order_by('-updated_at').first()

        if not payment:
            self.stdout.write(self.style.ERROR(f'No successful payments found for {email}'))
            self.stdout.write('Make a test payment first, or create a test payment in the admin.')
            return

        # Get the subscription if it exists
        subscription = None
        try:
            subscription = payment.subscription.first()
        except Exception:
            pass

        self.stdout.write(f'Sending test receipt to {email}...')
        self.stdout.write(f'Payment: {payment.reference}')
        self.stdout.write(f'Plan: {payment.plan.name}')
        self.stdout.write(f'Amount: {payment.amount / 100} {payment.currency}')

        # Send the receipt
        success = send_payment_receipt(payment, subscription=subscription)

        if success:
            self.stdout.write(self.style.SUCCESS(f'✓ Receipt sent successfully to {email}'))
            self.stdout.write(f'Check your email inbox (or console if using console email backend)')
        else:
            self.stdout.write(self.style.ERROR('✗ Failed to send receipt'))
