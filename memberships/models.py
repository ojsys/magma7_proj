from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    price_period = models.CharField(max_length=50, default='Per Month')
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, help_text='Featured image URL for the plan card')

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"

    def get_humanized_duration(self):
        """
        Return a human-readable duration format.
        """
        days = self.duration_days

        # Check for years
        if days >= 365:
            years = days // 365
            return f"{years} Year{'s' if years > 1 else ''}"

        # Check for months (approximate)
        if days >= 30:
            months = days // 30
            return f"{months} Month{'s' if months > 1 else ''}"

        # Check for weeks
        if days >= 7:
            weeks = days // 7
            return f"{weeks} Week{'s' if weeks > 1 else ''}"

        # Return days
        return f"{days} Day{'s' if days > 1 else ''}"


class PlanFeature(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.plan.name}: {self.text}"


class Subscription(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("upcoming", "Upcoming"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='upcoming')
    payment = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_reminder_days = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.plan} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.end_date:
            # If end_date not set, compute from start_date + plan duration
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        # Auto-update status
        today = timezone.localdate()
        if self.end_date < today:
            self.status = 'expired'
        elif self.start_date > today:
            self.status = 'upcoming'
        else:
            self.status = 'active'
        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        today = timezone.localdate()
        return (self.end_date - today).days

    @property
    def days_used(self):
        today = timezone.localdate()
        return (today - self.start_date).days


class WorkoutLog(models.Model):
    WORKOUT_TYPE_CHOICES = (
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_logs')
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPE_CHOICES)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    calories = models.PositiveIntegerField(null=True, blank=True, help_text='Calories burned')
    notes = models.TextField(blank=True)
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_workout_type_display()} ({self.date})"


class WeeklyGoal(models.Model):
    GOAL_TYPE_CHOICES = (
        ('workouts', 'Number of Workouts'),
        ('duration', 'Total Duration (minutes)'),
        ('calories', 'Total Calories'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weekly_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_value = models.PositiveIntegerField(help_text='Target value to achieve')
    week_start = models.DateField(default=timezone.localdate)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-week_start', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()}: {self.target_value}"

    @property
    def current_progress(self):
        """Calculate current progress towards the goal"""
        week_end = self.week_start + timedelta(days=7)
        workouts = WorkoutLog.objects.filter(
            user=self.user,
            date__gte=self.week_start,
            date__lt=week_end
        )

        if self.goal_type == 'workouts':
            return workouts.count()
        elif self.goal_type == 'duration':
            return workouts.aggregate(models.Sum('duration'))['duration__sum'] or 0
        elif self.goal_type == 'calories':
            return workouts.aggregate(models.Sum('calories'))['calories__sum'] or 0
        return 0

    @property
    def progress_percentage(self):
        """Calculate progress as percentage"""
        if self.target_value == 0:
            return 0
        return min(100, int((self.current_progress / self.target_value) * 100))


class WorkoutSession(models.Model):
    WORKOUT_TYPE_CHOICES = (
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    title = models.CharField(max_length=200)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPE_CHOICES)
    session_date = models.DateField()
    session_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    trainer = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['session_date', 'session_time']

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.session_date})"

    @property
    def is_upcoming(self):
        """Check if session is in the future"""
        from datetime import datetime
        session_datetime = datetime.combine(self.session_date, self.session_time)
        return session_datetime > timezone.now()
