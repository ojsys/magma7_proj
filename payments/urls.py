from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:plan_id>/', views.initiate_payment, name='initiate'),
    path('paystack/callback/', views.paystack_callback, name='paystack_callback'),
    path('stripe/success/', views.stripe_success, name='stripe_success'),
    path('stripe/cancel/', views.stripe_cancel, name='stripe_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
