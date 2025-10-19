# Quick Payment Setup Guide

## What Has Changed

The subscription flow now requires users to:
1. **Register/Login** before subscribing
2. **Complete payment** before membership activation
3. **Receive notifications** when payment succeeds

## How to Enable Payments

### Option 1: Test Mode (Recommended for Development)

1. **Copy the environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Get Paystack Test Keys** (for Nigeria/Africa):
   - Go to https://dashboard.paystack.com
   - Sign up or log in
   - Navigate to Settings > API Keys & Webhooks
   - Copy your **Test Public Key** (starts with `pk_test_`)
   - Copy your **Test Secret Key** (starts with `sk_test_`)

3. **Update `.env` file**:
   ```bash
   PAYMENTS_ENABLED=1
   PAYMENT_PROVIDER=paystack
   PAYSTACK_PUBLIC_KEY=pk_test_YOUR_KEY_HERE
   PAYSTACK_SECRET_KEY=sk_test_YOUR_KEY_HERE
   SITE_URL=http://127.0.0.1:8000
   CURRENCY=NGN
   ```

4. **Test with Paystack test cards**:
   - Card: 4084 0840 8408 4081
   - CVV: 408
   - Expiry: Any future date
   - OTP: 123456

### Option 2: Free Subscriptions (Testing Without Payment)

If you want to test other features without setting up payment:

```bash
PAYMENTS_ENABLED=0
```

This allows users to subscribe immediately without payment.

### Option 3: Stripe (International)

1. **Get Stripe Test Keys**:
   - Go to https://dashboard.stripe.com
   - Navigate to Developers > API Keys
   - Copy Publishable Key and Secret Key

2. **Update `.env` file**:
   ```bash
   PAYMENTS_ENABLED=1
   PAYMENT_PROVIDER=stripe
   STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY
   SITE_URL=http://127.0.0.1:8000
   CURRENCY=USD
   ```

3. **Test with Stripe test card**:
   - Card: 4242 4242 4242 4242
   - CVV: Any 3 digits
   - Expiry: Any future date

## Testing the Flow

1. **Start the server**:
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Open browser**: http://localhost:8000

3. **Test the subscription flow**:
   - Click "Choose Plan" on any membership plan
   - If not logged in, you'll be redirected to register
   - After registration, you'll be taken to payment gateway
   - Complete payment with test card
   - You'll be redirected to dashboard with active subscription

4. **Check notifications**:
   - Click the bell icon in dashboard
   - You should see "Payment Successful" notification

## Admin Interface

View payments and subscriptions:
1. Go to http://localhost:8000/admin
2. Navigate to "Payments" to see all transactions
3. Navigate to "Subscriptions" to see which payments created subscriptions

## Production Checklist

When going live:

- [ ] Get **live** API keys from payment provider
- [ ] Update `.env` with live keys (pk_live_xxx, sk_live_xxx)
- [ ] Set `PAYMENTS_ENABLED=1`
- [ ] Update `SITE_URL` to your production domain (https://yourdomain.com)
- [ ] Ensure your site uses HTTPS (required for payments)
- [ ] Configure webhooks in payment provider dashboard
- [ ] Test with small real payment first
- [ ] Add `.env` to `.gitignore` (never commit secrets!)

## Troubleshooting

**"Payment gateway not configured"**
- Make sure you've added keys to `.env` file
- Restart the Django server after updating `.env`

**Payment succeeds but subscription not created**
- Check that callback URL is accessible
- Review payment details in admin panel
- Check Django logs for errors

**Can't find .env file**
- Make sure you ran: `cp .env.example .env`
- The `.env` file should be in the same directory as manage.py

## Support

Need help?
- Check `SUBSCRIPTION_FLOW.md` for detailed technical documentation
- Review payment details in admin panel at `/admin/payments/payment/`
- Check Django console logs for errors

## Summary

The new flow ensures:
✓ Users must register before subscribing
✓ Payment is required before activation (when enabled)
✓ All payments are tracked in database
✓ Users receive notifications on success
✓ Subscriptions are linked to payments
✓ Easy to switch between test and production
