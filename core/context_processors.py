from django.conf import settings


def settings_vars(request):
    currency = getattr(settings, 'CURRENCY', 'NGN')
    symbols = {
        'NGN': '₦',
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
    }
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Magma7Fitness'),
        'CURRENCY': currency,
        'CURRENCY_SYMBOL': symbols.get(currency.upper(), ''),
        'PAYMENTS_ENABLED': getattr(settings, 'PAYMENTS_ENABLED', False),
        'PAYMENT_PROVIDER': getattr(settings, 'PAYMENT_PROVIDER', 'paystack'),
    }

