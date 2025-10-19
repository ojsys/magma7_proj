# Magma7Fitness Subscription Flow Documentation

## Overview

The subscription flow has been designed to require immediate payment before membership activation, with automatic notification capture. Users must register and complete payment before gaining access to their membership.

## User Flow

### 1. User Selects a Plan

**Location**: Home page (`/`) or Plans page (`/memberships/plans/`)

When a user clicks "Choose Plan" on any membership plan, they are directed to:
```
/memberships/subscribe/<plan_id>/
```

### 2. Authentication Check

The `subscribe` view performs the following checks:

**For Non-Authenticated Users:**
- Redirects to registration page: `/accounts/register/?next=/memberships/subscribe/<plan_id>/`
- After successful registration, user is redirected back to the subscribe URL
- This ensures user account exists before payment

**For Authenticated Users:**
- Proceeds to payment gateway to complete payment.
- Subscription only activates after successful payment confirmation.

### 3. Payment Gateway Integration

When `PAYMENTS_ENABLED=1` in settings:

**Step 1: Payment Initialization**
- User is redirected to `/payments/initiate/<plan_id>/`
- System creates a Payment record with status="pending"
- Generates unique payment reference (e.g., `M7_a1b2c3d4e5f6g7h8`)

**Step 2: Gateway Redirect**
- **Paystack**: User redirected to Paystack checkout page
- **Stripe**: User redirected to Stripe checkout session
- User completes payment on secure gateway page

**Step 3: Payment Verification**
- **Paystack**: Callback to `/payments/paystack/callback/?reference=M7_xxx`
- **Stripe**: Success redirect to `/payments/stripe/success/?session_id=cs_xxx`
- System verifies payment with gateway API
- Payment record updated to status="successful"

**Step 4: Subscription Activation**
- Subscription created and linked to payment
- Start date: Today
- End date: Today + plan.duration_days
- Status: Auto-calculated (active/upcoming based on dates)

**Step 5: User Notification**
- In-app notification created
- Email notification sent (if configured)
- Success message displayed on dashboard

### 4. Subscription Created

User is redirected to dashboard with:
- Active subscription displayed
- Success message: "Payment successful. Subscription active until {end_date}."
- Notification: "Your payment for {plan_name} was successful. Your membership is now active!"

## Technical Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Clicks "Choose Plan"                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      v
         ┌────────────────────────────┐
         │  GET /memberships/          │
         │  subscribe/<plan_id>/       │
         └────────────┬───────────────┘
                      │
         ┌────────────v────────────┐
         │  Is user authenticated?  │
         └─┬────────────────────┬──┘
           │ NO                 │ YES
           v                    v
    ┌──────────────┐    ┌──────────────────┐
    │ Redirect to  │    │ Check if         │
    │ register with│    │ PAYMENTS_ENABLED │
    │ ?next=...    │    └─┬────────────┬───┘
    └──────┬───────┘      │ YES        │ NO
           │              v            v
           │      ┌───────────────┐   ┌──────────────┐
           │      │ Redirect to   │   │ Create sub   │
           │      │ /payments/    │   │ immediately  │
           │      │ initiate/...  │   └──────┬───────┘
           │      └───────┬───────┘          │
           │              │                  │
    ┌──────v──────────────v───────┐         │
    │ User Registers/Logs In       │         │
    └──────┬───────────────────────┘         │
           │                                 │
           v                                 │
    ┌──────────────────────┐                │
    │ Redirect back to     │                │
    │ subscribe URL        │                │
    └──────┬───────────────┘                │
           │                                 │
           v                                 │
    ┌───────────────────────┐               │
    │ Create Payment record │               │
    │ status=pending        │               │
    └───────┬───────────────┘               │
            │                                │
            v                                │
    ┌──────────────────┐                    │
    │ Redirect to      │                    │
    │ Gateway Checkout │                    │
    │ (Paystack/Stripe)│                    │
    └────────┬─────────┘                    │
             │                               │
             v                               │
    ┌────────────────┐                      │
    │ User Completes │                      │
    │ Payment        │                      │
    └────────┬───────┘                      │
             │                               │
             v                               │
    ┌──────────────────┐                    │
    │ Gateway Callback │                    │
    │ Verify Payment   │                    │
    └────────┬─────────┘                    │
             │                               │
             v                               │
    ┌──────────────────┐                    │
    │ Mark Payment     │                    │
    │ successful       │                    │
    └────────┬─────────┘                    │
             │                               │
             v                               │
    ┌──────────────────┐                    │
    │ Create           │<───────────────────┘
    │ Subscription     │
    │ Link Payment     │
    └────────┬─────────┘
             │
             v
    ┌──────────────────┐
    │ Send             │
    │ Notification     │
    └────────┬─────────┘
             │
             v
    ┌──────────────────┐
    │ Redirect to      │
    │ Dashboard        │
    └──────────────────┘
```

## Database Schema

### Payment Model
```python
{
    'user': ForeignKey(User),
    'plan': ForeignKey(Plan),
    'amount': Integer,  # In minor units (kobo/cents)
    'currency': String,  # 'NGN', 'USD', etc.
    'provider': String,  # 'paystack' or 'stripe'
    'status': String,  # 'pending', 'successful', 'failed', 'cancelled'
    'reference': String,  # Unique payment reference
    'gateway_response': JSON,  # Full gateway response
    'created_at': DateTime,
    'completed_at': DateTime,
}
```

### Subscription Model
```python
{
    'user': ForeignKey(User),
    'plan': ForeignKey(Plan),
    'payment': ForeignKey(Payment),  # Links to payment
    'start_date': Date,
    'end_date': Date,
    'status': String,  # 'active', 'expired', 'upcoming', 'cancelled'
    'created_at': DateTime,
}
```

## Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Key settings:

```bash
# Enable/disable payment requirement
PAYMENTS_ENABLED=1  # 1 = require payment, 0 = free subscriptions

# Choose payment provider
PAYMENT_PROVIDER=paystack  # or 'stripe'

# Site URL for callbacks
SITE_URL=http://127.0.0.1:8000

# Currency
CURRENCY=NGN  # or USD, GBP, etc.

# Provider keys (get from dashboard)
PAYSTACK_PUBLIC_KEY=pk_test_xxx
PAYSTACK_SECRET_KEY=sk_test_xxx

STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## Testing the Flow

### Payments Disabled

Set in `.env`:
```bash
PAYMENTS_ENABLED=0
```

Behavior:
- Users cannot complete subscription while payments are disabled.
- The system will redirect back to the plans page with an error message.
- Enable payments and configure a provider to allow subscriptions.

### Test Mode with Payment Gateway

1. **Paystack Test Mode**:
   - Use test API keys (pk_test_xxx, sk_test_xxx)
   - Test card: 4084 0840 8408 4081
   - CVV: 408, Expiry: Any future date
   - OTP: 123456

2. **Stripe Test Mode**:
   - Use test API keys
   - Test card: 4242 4242 4242 4242
   - CVV: Any 3 digits, Expiry: Any future date

### Production Setup

1. Get live API keys from gateway dashboard
2. Update `.env` with live keys
3. Set `PAYMENTS_ENABLED=1`
4. Update `SITE_URL` to production domain
5. Configure webhooks:
   - Paystack: Add webhook URL in dashboard
   - Stripe: Create webhook endpoint, add secret to `.env`

## Error Handling

### Payment Failures

If payment fails:
- Payment status set to "failed"
- Error message displayed to user
- User redirected back to plans page
- No subscription created

### Gateway Connection Issues

If gateway is unreachable:
- Payment marked as failed with exception details
- User-friendly error message displayed
- Admin can view full error in gateway_response field

### Duplicate Payments

System prevents duplicate subscriptions by:
- Checking payment status before creating subscription
- Using unique payment references
- Webhook idempotency (won't create duplicate subs)

## Notifications

After successful payment, user receives:

1. **Success Message**: Flash message on dashboard
2. **In-App Notification**: Visible in notification dropdown
3. **Email Notification**: (if email configured)

Example notification:
```
Title: Payment Successful
Body: Your payment for Premium Plan was successful. Your membership is now active!
```

## Admin Interface

### Viewing Subscriptions

Admin can see:
- All subscriptions with payment status
- Payment reference and provider
- Link to payment details
- Subscription dates and status

### Viewing Payments

Admin can see:
- All payment transactions
- Gateway responses (for debugging)
- Amount in readable format (converted from minor units)
- Payment timeline (created, completed)

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/memberships/subscribe/<plan_id>/` | GET | Initiate subscription flow |
| `/payments/initiate/<plan_id>/` | GET | Create payment and redirect to gateway |
| `/payments/paystack/callback/` | GET | Paystack payment verification |
| `/payments/stripe/success/` | GET | Stripe payment success |
| `/payments/stripe/cancel/` | GET | Stripe payment cancellation |
| `/payments/stripe/webhook/` | POST | Stripe webhook handler |

## Security Considerations

1. **Payment References**: Cryptographically secure random tokens
2. **Gateway Verification**: All payments verified via gateway API
3. **CSRF Protection**: All forms protected with Django CSRF tokens
4. **User Verification**: Payments must match logged-in user
5. **Webhook Security**: Stripe webhooks verified with signature
6. **SSL Required**: Production must use HTTPS for payment pages

## Troubleshooting

### "Payment gateway not configured" error
- Check that PAYSTACK_SECRET_KEY or STRIPE_SECRET_KEY is set in `.env`
- Verify keys are not empty strings

### Payment succeeds but no subscription created
- Check webhook configuration (for Stripe)
- Verify payment callback URL is accessible
- Check logs for errors in payment verification

### User stuck after payment
- Verify SITE_URL in `.env` matches actual domain
- Check callback URLs are not blocked by firewall
- Review payment gateway_response in admin

## Support

For issues:
1. Check Django logs for errors
2. Review payment gateway_response in admin
3. Verify all environment variables are set
4. Test with gateway test cards first
5. Check gateway dashboard for transaction details
