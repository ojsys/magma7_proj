from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    PROVIDERS = (
        ("paystack", "Paystack"),
        ("stripe", "Stripe"),
    )
    STATUSES = (
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey('memberships.Plan', on_delete=models.PROTECT, related_name='payments')
    amount = models.PositiveIntegerField(help_text="Minor units (kobo for NGN, cents for USD)")
    currency = models.CharField(max_length=10, default='NGN')
    provider = models.CharField(max_length=10, choices=PROVIDERS)
    status = models.CharField(max_length=12, choices=STATUSES, default='pending')
    reference = models.CharField(max_length=100, unique=True)
    gateway_response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_success(self, response: dict | None = None):
        self.status = 'successful'
        self.completed_at = timezone.now()
        if response is not None:
            self.gateway_response = response
        self.save(update_fields=['status', 'completed_at', 'gateway_response', 'updated_at'])

    def mark_failed(self, response: dict | None = None):
        self.status = 'failed'
        if response is not None:
            self.gateway_response = response
        self.save(update_fields=['status', 'gateway_response', 'updated_at'])

