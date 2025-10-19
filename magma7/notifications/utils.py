from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def notify_user(user, title: str, body: str, email: bool = True, in_app: bool = True):
    if in_app:
        Notification.objects.create(user=user, title=title, body=body)
    if email and user.email:
        send_mail(
            subject=f"{getattr(settings, 'SITE_NAME', 'Magma7Fitness')}: {title}",
            message=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@magma7fitness.local'),
            recipient_list=[user.email],
            fail_silently=True,
        )

