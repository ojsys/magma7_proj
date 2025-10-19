from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Sum, Count
from django.http import JsonResponse

from django.conf import settings
from .models import Plan, Subscription, WorkoutLog, WeeklyGoal, WorkoutSession
from notifications.utils import notify_user


def plan_list(request):
    plans = Plan.objects.filter(is_active=True).order_by('price')
    return render(request, 'memberships/plans.html', {'plans': plans})


def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    return render(request, 'memberships/plan_detail.html', {"plan": plan})


@login_required
def dashboard(request):
    from notifications.models import Notification

    sub = Subscription.objects.filter(user=request.user).order_by('-created_at').first()

    # Get recent notifications (last 10)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # Initialize default values
    calories_burned = 0
    workouts_this_month = 0
    streak_days = 0
    total_hours = 0
    recent_workouts = []

    try:
        # Get workout statistics
        today = timezone.localdate()
        week_start = today - timedelta(days=7)
        month_start = today - timedelta(days=30)

        # Calories burned this week
        calories_burned = WorkoutLog.objects.filter(
            user=request.user,
            date__gte=week_start
        ).aggregate(total=Sum('calories'))['total'] or 0

        # Workouts this month
        workouts_this_month = WorkoutLog.objects.filter(
            user=request.user,
            date__gte=month_start
        ).count()

        # Calculate streak
        current_date = today
        while True:
            if WorkoutLog.objects.filter(user=request.user, date=current_date).exists():
                streak_days += 1
                current_date -= timedelta(days=1)
            else:
                break

        # Total hours
        total_duration = WorkoutLog.objects.filter(
            user=request.user
        ).aggregate(total=Sum('duration'))['total'] or 0
        total_hours = round(total_duration / 60, 1)

        # Recent workouts
        recent_workouts = WorkoutLog.objects.filter(user=request.user)[:3]

    except Exception as e:
        # If WorkoutLog table doesn't exist yet, use default values
        print(f"Warning: Could not fetch workout data: {e}")

    # Get weekly goals
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())  # Start of current week (Monday)
    weekly_goals = WeeklyGoal.objects.filter(
        user=request.user,
        is_active=True,
        week_start=week_start
    )

    # Get upcoming sessions
    upcoming_sessions = WorkoutSession.objects.filter(
        user=request.user,
        session_date__gte=today
    )[:5]

    ctx = {
        'subscription': sub,
        'calories_burned': calories_burned,
        'workouts_this_month': workouts_this_month,
        'streak_days': streak_days,
        'total_hours': total_hours,
        'recent_workouts': recent_workouts,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
        'weekly_goals': weekly_goals,
        'upcoming_sessions': upcoming_sessions,
    }
    return render(request, 'memberships/dashboard.html', ctx)


def subscribe(request, plan_id):
    """
    Handle subscription flow - redirect to payment if payments enabled,
    or require login first for non-authenticated users.
    """
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)

    # If user is not authenticated, redirect to login/register with next parameter
    if not request.user.is_authenticated:
        from django.urls import reverse
        login_url = reverse('users:signup')  # Signup page
        next_url = reverse('memberships:subscribe', kwargs={'plan_id': plan_id})
        return redirect(f"{login_url}?next={next_url}")

    # Always initiate payment flow; activation occurs after successful payment
    return redirect('payments:initiate', plan_id=plan.id)


@login_required
def my_subscription(request):
    sub = Subscription.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'memberships/my_subscription.html', {"subscription": sub})


@login_required
def renew(request, plan_id):
    plan = get_object_or_404(Plan, pk=plan_id, is_active=True)
    last = Subscription.objects.filter(user=request.user).order_by('-end_date').first()
    start = timezone.localdate()
    if last and last.end_date >= start:
        start = last.end_date + timedelta(days=1)
    end = start + timedelta(days=plan.duration_days)
    sub = Subscription.objects.create(user=request.user, plan=plan, start_date=start, end_date=end)
    messages.success(request, f"Renewed {plan.name}. New period {sub.start_date} to {sub.end_date}.")
    notify_user(request.user, title="Subscription Renewed", body=f"Your plan {plan.name} renewed until {sub.end_date}.")
    return redirect('memberships:dashboard')


@login_required
def log_workout(request):
    if request.method == 'POST':
        workout_type = request.POST.get('workout_type')
        duration = request.POST.get('duration')
        calories = request.POST.get('calories') or None
        notes = request.POST.get('notes', '')

        WorkoutLog.objects.create(
            user=request.user,
            workout_type=workout_type,
            duration=int(duration),
            calories=int(calories) if calories else None,
            notes=notes
        )

        messages.success(request, 'Workout logged successfully!')
        return redirect('memberships:dashboard')

    return redirect('memberships:dashboard')


@login_required
def all_activities(request):
    """View all workout activities"""
    from notifications.models import Notification

    # Get all workout logs for the user, paginated
    all_workouts = WorkoutLog.objects.filter(user=request.user).order_by('-date', '-created_at')

    # Calculate total stats
    total_workouts = all_workouts.count()
    total_duration = all_workouts.aggregate(total=Sum('duration'))['total'] or 0
    total_calories = all_workouts.aggregate(total=Sum('calories'))['total'] or 0
    total_hours = round(total_duration / 60, 1)

    # Get notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    ctx = {
        'all_workouts': all_workouts,
        'total_workouts': total_workouts,
        'total_hours': total_hours,
        'total_calories': total_calories,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'memberships/all_activities.html', ctx)


@login_required
def profile(request):
    """User profile update page"""
    from notifications.models import Notification

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('memberships:profile')

    # Get notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    ctx = {
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'memberships/profile.html', ctx)


@login_required
def settings(request):
    """User settings page"""
    from notifications.models import Notification

    if request.method == 'POST':
        # Handle settings updates (e.g., notification preferences, password change)
        action = request.POST.get('action')

        if action == 'change_password':
            from django.contrib.auth import update_session_auth_hash
            from django.contrib.auth.forms import PasswordChangeForm

            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Password changed successfully!')
            else:
                for error in form.errors.values():
                    messages.error(request, error[0])
            return redirect('memberships:settings')

    # Get notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    ctx = {
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'memberships/settings.html', ctx)
