from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from memberships.models import Subscription
from notifications.utils import notify_user


REMINDER_WINDOWS = {7, 3, 1, 0}


class Command(BaseCommand):
    help = "Send membership expiry reminders via email and in-app notifications."

    def handle(self, *args, **options):
        today = timezone.localdate()
        count = 0
        for sub in Subscription.objects.select_related('user', 'plan').all():
            # Refresh status
            previous_status = sub.status
            sub.save()  # updates status based on dates
            days_remaining = (sub.end_date - today).days

            if days_remaining in REMINDER_WINDOWS:
                if sub.last_reminder_days != days_remaining:
                    if days_remaining > 0:
                        title = f"Your {{sub.plan.name}} plan expires in {days_remaining} day(s)"
                        body = (
                            f"Hi {sub.user.first_name or sub.user.username}, your {sub.plan.name} plan "
                            f"will expire on {sub.end_date}. Renew to stay active."
                        )
                    elif days_remaining == 0:
                        title = f"Your {sub.plan.name} plan expires today"
                        body = (
                            f"Hi {sub.user.first_name or sub.user.username}, your {sub.plan.name} plan "
                            f"expires today ({sub.end_date}). Renew to avoid interruption."
                        )
                    else:
                        title = f"Your {sub.plan.name} plan has expired"
                        body = (
                            f"Hi {sub.user.first_name or sub.user.username}, your {sub.plan.name} plan expired on "
                            f"{sub.end_date}. Renew anytime to reactivate."
                        )
                    notify_user(sub.user, title=title, body=body, email=True, in_app=True)
                    sub.last_reminder_days = days_remaining
                    sub.save(update_fields=["last_reminder_days", "updated_at", "status", "end_date", "start_date"])
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Sent {count} reminders."))

