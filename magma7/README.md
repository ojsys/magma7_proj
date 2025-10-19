Magma7Fitness — Django App
==========================

Features
- Modern Light Theme UI with professional design
- Public pages: Home, About, Facilities, Team, Mission, Vision, Values
- Memberships: Plans, subscribe, renew, dashboard, my subscription, plan detail pages
- Users: Signup, login/logout (Django auth), profile auto-created
- Notifications: In‑app + email reminders for expiring memberships (bell with unread badge, mark-all-read)
- Admin: Manage plans, subscriptions, notifications, profiles
- CMS: Editable homepage hero, programs, services, testimonials, and rich pages via Django admin
- **Free Guide**: Clickable call-to-action in hero section with admin management

Quickstart
1) Create/activate a virtualenv and install dependencies:
   - macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
   - Windows (PowerShell): `python -m venv venv; .\\venv\\Scripts\\Activate.ps1`
   - Install: `pip install -r requirements.txt`

2) Run migrations and create admin:
   - `cd magma7`
   - `python manage.py makemigrations`
   - `python manage.py migrate`
   - `python manage.py createsuperuser`

3) Run the server:
   - `python manage.py runserver`
   - Open http://127.0.0.1:8000

4) Seed plans (optional):
   - Use Django admin at `/admin/` to create `Plan` items, or run:
   - `python manage.py seed_plans`
   - `python manage.py seed_cms`
   - Seed CMS content (hero/programs/services/testimonials):
   - `python manage.py seed_cms`

Email configuration
- Defaults to console backend (emails print to terminal).
- To send real emails set environment variables (e.g., in a `.env` loaded by your process manager):
  - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
  - `EMAIL_HOST=smtp.yourhost.com`
  - `EMAIL_PORT=587`
  - `EMAIL_USE_TLS=1`
  - `EMAIL_HOST_USER=you@example.com`
  - `EMAIL_HOST_PASSWORD=yourpassword`
  - `DEFAULT_FROM_EMAIL=info@magma7fitness.com`

Reminder scheduler
- Command: `python manage.py send_reminders`
- Logic: sends notifications at 7, 3, 1, and 0 days before expiry.
- Schedule with cron (example, every day at 09:00):
  - `0 9 * * * /path/to/venv/bin/python /path/to/magma7/manage.py send_reminders >> /var/log/magma7_reminders.log 2>&1`

Project layout
- `magma7/` project settings, URLs, `manage.py`
- `core/` static content pages
- `memberships/` plans, subscriptions, reminder command
- `notifications/` Notification model, list view, email utility
- `payments/` Payment model, initiation + callbacks for Paystack/Stripe
- `users/` signup, profiles (OneToOne with User)
- `templates/` base, auth templates, pages
- `static/` CSS overrides
- `cms/` lightweight CMS models, testimonials, and pages

Notes
- Materialize assets load from CDN; ensure internet access in production.
- Password reset pages use Django’s auth URLs; add templates under `templates/registration/` if you want to customize.

Payments
- Toggle payments via env: `PAYMENTS_ENABLED=1`
- Provider (default Paystack): `PAYMENT_PROVIDER=paystack` or `stripe`
- Common env:
  - `SITE_URL` (e.g., `http://127.0.0.1:8000` or your domain)
  - `CURRENCY` (`NGN` for Paystack; `USD` etc. for Stripe)

Paystack setup
- `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY`
- Flow: Plan → payment initiation → redirect to Paystack → callback verifies and activates subscription.

Stripe setup
- `pip install stripe` (already listed in requirements)
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`
- Webhook endpoint: set to `{{SITE_URL}}/payments/stripe/webhook/` in your Stripe dashboard.
- Flow: Plan → Checkout Session → success URL or webhook verifies and activates subscription (idempotent).

Usage
- With payments disabled (default), choosing a plan immediately creates a subscription.
- With payments enabled, users are redirected to the provider checkout; subscription is created after successful payment.
- Paystack uses the callback URL to confirm. Stripe can confirm via success page and/or webhook; webhook recommended in production.

CMS editing
- Go to `/admin/` → CMS section to edit:
  - Site Settings (brand, colors, hero content)
  - Programs and Services (home sections)
  - Testimonials (ratings)
  - Rich Pages (e.g., About content)
