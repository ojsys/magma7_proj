import csv
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import MemberProfile

User = get_user_model()


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "date_of_birth")
    search_fields = ("user__username", "user__email")


# Extend the default User admin with CSV export
def _to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        s = value.strip().lower()
        if s in {"1", "true", "t", "yes", "y", "on"}:
            return True
        if s in {"0", "false", "f", "no", "n", "off", ""}:
            return False
        return bool(s)
    return bool(value)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active_icon', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Disable date_hierarchy to avoid MySQL timezone table requirement on cPanel
    # date_hierarchy = 'date_joined'
    ordering = ('-date_joined',)
    actions = ['export_users_csv', 'export_users_with_subscriptions_csv']

    # Safe boolean display to avoid KeyError when DB stores '1'/'0' as TEXT
    def is_active_icon(self, obj):
        return _to_bool(getattr(obj, 'is_active', False))

    is_active_icon.boolean = True
    is_active_icon.short_description = 'Active'
    is_active_icon.admin_order_field = 'is_active'

    def is_staff_icon(self, obj):
        return _to_bool(getattr(obj, 'is_staff', False))

    is_staff_icon.boolean = True
    is_staff_icon.short_description = 'Staff'
    is_staff_icon.admin_order_field = 'is_staff'

    def is_superuser_icon(self, obj):
        return _to_bool(getattr(obj, 'is_superuser', False))

    is_superuser_icon.boolean = True
    is_superuser_icon.short_description = 'Superuser'
    is_superuser_icon.admin_order_field = 'is_superuser'

    def get_list_display(self, request):
        cols = list(super().get_list_display(request))
        mapping = {
            'is_active': 'is_active_icon',
            'is_staff': 'is_staff_icon',
            'is_superuser': 'is_superuser_icon',
        }
        for i, name in enumerate(cols):
            if name in mapping:
                cols[i] = mapping[name]
        return tuple(cols)

    def export_users_csv(self, request, queryset):
        """Export selected users basic information to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'users_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'First Name', 'Last Name',
            'Phone', 'Date of Birth', 'Address', 'Is Active', 'Date Joined', 'Last Login'
        ])

        for user in queryset:
            try:
                profile = user.profile
                phone = profile.phone
                dob = profile.date_of_birth
                address = profile.address
            except:
                phone = 'N/A'
                dob = 'N/A'
                address = 'N/A'

            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                phone,
                dob,
                address,
                'Yes' if user.is_active else 'No',
                user.date_joined,
                user.last_login or 'Never',
            ])

        return response
    export_users_csv.short_description = "Export selected users to CSV"

    def export_users_with_subscriptions_csv(self, request, queryset):
        """Export selected users with their subscription details to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'users_subscriptions_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'First Name', 'Last Name',
            'Phone', 'Active Subscription', 'Plan Name', 'Subscription Status',
            'Start Date', 'End Date', 'Days Remaining', 'Total Workouts',
            'Date Joined', 'Last Login'
        ])

        for user in queryset:
            # Get profile info
            try:
                profile = user.profile
                phone = profile.phone
            except:
                phone = 'N/A'

            # Get active subscription
            from memberships.models import Subscription, WorkoutLog
            active_sub = Subscription.objects.filter(user=user).order_by('-created_at').first()

            # Get workout count
            workout_count = WorkoutLog.objects.filter(user=user).count()

            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                phone,
                'Yes' if active_sub else 'No',
                active_sub.plan.name if active_sub else 'N/A',
                active_sub.status if active_sub else 'N/A',
                active_sub.start_date if active_sub else 'N/A',
                active_sub.end_date if active_sub else 'N/A',
                active_sub.days_remaining if active_sub else 'N/A',
                workout_count,
                user.date_joined,
                user.last_login or 'Never',
            ])

        return response
    export_users_with_subscriptions_csv.short_description = "Export users with subscription details to CSV"


# Register custom user admin (unregister default first if needed)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)
