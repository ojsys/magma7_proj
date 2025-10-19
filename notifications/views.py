from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def list_notifications(request):
    # Auto-mark unread as read when visiting the page
    request.user.notifications.filter(is_read=False).update(is_read=True)
    qs = request.user.notifications.all()
    return render(request, 'notifications/list.html', {"notifications": qs})


@login_required
def mark_all_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('notifications:list')
