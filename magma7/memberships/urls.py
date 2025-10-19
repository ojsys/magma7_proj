from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('plans/', views.plan_list, name='plans'),
    path('plans/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('my-subscription/', views.my_subscription, name='my_subscription'),
    path('renew/<int:plan_id>/', views.renew, name='renew'),
    path('log-workout/', views.log_workout, name='log_workout'),
    path('all-activities/', views.all_activities, name='all_activities'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
]
