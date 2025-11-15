import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Plan, Subscription, PlanFeature, WorkoutLog, WeeklyGoal, WorkoutSession


def _to_bool(value):
    """Coerce various truthy/falsey representations to a Python bool.
    Handles strings like '0'/'1', 'true'/'false', numbers, and actual booleans.
    """
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
        # Fallback for unexpected strings
        return bool(s)
    return bool(value)


def export_to_csv(modeladmin, request, queryset, fields, filename):
    """
    Generic CSV export function for admin actions
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)

    # Write header
    writer.writerow(fields)

    # Write data rows
    for obj in queryset:
        row = []
        for field in fields:
            # Handle nested attributes (e.g., 'user.email')
            if '.' in field:
                value = obj
                for attr in field.split('.'):
                    value = getattr(value, attr, '')
                row.append(value)
            else:
                value = getattr(obj, field, '')
                row.append(value)
        writer.writerow(row)

    return response


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "price_period", "duration_days", "is_featured_icon", "is_active_icon")
    list_filter = ("is_active", "is_featured")
    search_fields = ("name",)
    fields = ("name", "description", "price", "price_period", "duration_days", "is_active", "is_featured", "image_url")
    inlines = [PlanFeatureInline]

    # Defensive boolean display to avoid KeyError when DB stores '0'/'1' strings
    def is_featured_icon(self, obj):
        return _to_bool(getattr(obj, "is_featured", False))

    is_featured_icon.boolean = True
    is_featured_icon.short_description = "Featured"
    is_featured_icon.admin_order_field = "is_featured"

    def is_active_icon(self, obj):
        return _to_bool(getattr(obj, "is_active", False))

    is_active_icon.boolean = True
    is_active_icon.short_description = "Active"
    is_active_icon.admin_order_field = "is_active"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "status", "payment_status", "created_at")
    list_filter = ("status", "plan", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at", "payment_info")
    # date_hierarchy = "created_at"  # Disabled due to MySQL timezone tables not being populated
    actions = ['export_subscriptions_csv']

    def payment_status(self, obj):
        if obj.payment:
            return obj.payment.status
        return "No payment"
    payment_status.short_description = "Payment"

    def payment_info(self, obj):
        if obj.payment:
            return f"Payment: {obj.payment.reference} - {obj.payment.status} ({obj.payment.provider})"
        return "No payment linked"
    payment_info.short_description = "Payment Details"

    def export_subscriptions_csv(self, request, queryset):
        """Export selected subscriptions to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'subscriptions_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'First Name', 'Last Name',
            'Plan Name', 'Plan Price', 'Start Date', 'End Date', 'Status',
            'Days Remaining', 'Payment Reference', 'Payment Status', 'Payment Amount',
            'Created At'
        ])

        for sub in queryset:
            writer.writerow([
                sub.user.id,
                sub.user.username,
                sub.user.email,
                sub.user.first_name,
                sub.user.last_name,
                sub.plan.name,
                sub.plan.price,
                sub.start_date,
                sub.end_date,
                sub.status,
                sub.days_remaining,
                sub.payment.reference if sub.payment else 'N/A',
                sub.payment.status if sub.payment else 'N/A',
                f"{sub.payment.amount / 100:.2f}" if sub.payment else 'N/A',
                sub.created_at,
            ])

        return response
    export_subscriptions_csv.short_description = "Export selected subscriptions to CSV"


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ("user", "workout_type", "duration", "calories", "date", "created_at")
    list_filter = ("workout_type", "date")
    search_fields = ("user__username", "user__email", "notes")
    # date_hierarchy = "date"  # Disabled due to MySQL timezone tables not being populated
    readonly_fields = ("created_at",)
    actions = ['export_workout_logs_csv']

    def export_workout_logs_csv(self, request, queryset):
        """Export selected workout logs to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'workout_logs_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'Workout Type', 'Duration (min)',
            'Calories Burned', 'Date', 'Notes', 'Created At'
        ])

        for log in queryset:
            writer.writerow([
                log.user.id,
                log.user.username,
                log.user.email,
                log.get_workout_type_display(),
                log.duration,
                log.calories or 'N/A',
                log.date,
                log.notes,
                log.created_at,
            ])

        return response
    export_workout_logs_csv.short_description = "Export selected workout logs to CSV"


@admin.register(WeeklyGoal)
class WeeklyGoalAdmin(admin.ModelAdmin):
    list_display = ("user", "goal_type", "target_value", "week_start", "is_active_icon", "created_at")
    list_filter = ("goal_type", "is_active", "week_start")
    search_fields = ("user__username", "user__email")
    # date_hierarchy = "week_start"  # Disabled due to MySQL timezone tables not being populated
    readonly_fields = ("created_at",)
    actions = ['export_weekly_goals_csv']

    def is_active_icon(self, obj):
        return _to_bool(getattr(obj, "is_active", False))

    is_active_icon.boolean = True
    is_active_icon.short_description = "Active"
    is_active_icon.admin_order_field = "is_active"

    def export_weekly_goals_csv(self, request, queryset):
        """Export selected weekly goals to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'weekly_goals_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'Goal Type', 'Target Value',
            'Current Progress', 'Progress %', 'Week Start', 'Is Active', 'Created At'
        ])

        for goal in queryset:
            writer.writerow([
                goal.user.id,
                goal.user.username,
                goal.user.email,
                goal.get_goal_type_display(),
                goal.target_value,
                goal.current_progress,
                goal.progress_percentage,
                goal.week_start,
                'Yes' if goal.is_active else 'No',
                goal.created_at,
            ])

        return response
    export_weekly_goals_csv.short_description = "Export selected weekly goals to CSV"


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "workout_type", "session_date", "session_time", "duration", "trainer")
    list_filter = ("workout_type", "session_date")
    search_fields = ("user__username", "user__email", "title", "trainer")
    # date_hierarchy = "session_date"  # Disabled due to MySQL timezone tables not being populated
    readonly_fields = ("created_at",)
    actions = ['export_workout_sessions_csv']

    def export_workout_sessions_csv(self, request, queryset):
        """Export selected workout sessions to CSV"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'workout_sessions_export_{timestamp}.csv'

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            'User ID', 'Username', 'Email', 'Session Title', 'Workout Type',
            'Session Date', 'Session Time', 'Duration (min)', 'Trainer', 'Notes', 'Created At'
        ])

        for session in queryset:
            writer.writerow([
                session.user.id,
                session.user.username,
                session.user.email,
                session.title,
                session.get_workout_type_display(),
                session.session_date,
                session.session_time,
                session.duration,
                session.trainer or 'N/A',
                session.notes,
                session.created_at,
            ])

        return response
    export_workout_sessions_csv.short_description = "Export selected workout sessions to CSV"
