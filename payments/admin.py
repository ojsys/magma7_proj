import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "provider", "amount_display", "currency", "status", "reference", "created_at")
    list_filter = ("provider", "status", "currency", "created_at")
    search_fields = ("user__username", "user__email", "reference")
    readonly_fields = ("created_at", "updated_at", "completed_at", "gateway_response")
    # date_hierarchy = "created_at"  # Disabled due to MySQL timezone tables not being populated
    actions = ['export_payments_csv']

    def amount_display(self, obj):
        """Convert minor units to major units for display"""
        return f"{obj.amount / 100:.2f}"
    amount_display.short_description = "Amount"

    def export_payments_csv(self, request, queryset):
        """Export selected payments to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'payments_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'Payment ID', 'User ID', 'Username', 'Email', 'Plan Name',
            'Amount', 'Currency', 'Provider', 'Status', 'Reference',
            'Created At', 'Completed At'
        ])

        for payment in queryset:
            writer.writerow([
                payment.id,
                payment.user.id,
                payment.user.username,
                payment.user.email,
                payment.plan.name,
                f"{payment.amount / 100:.2f}",
                payment.currency,
                payment.provider,
                payment.status,
                payment.reference,
                payment.created_at,
                payment.completed_at or 'N/A',
            ])

        return response
    export_payments_csv.short_description = "Export selected payments to CSV"

