from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('facilities/', views.facilities, name='facilities'),
    path('team/', views.team, name='team'),
    path('careers/', views.careers, name='careers'),
    path('mission/', views.mission, name='mission'),
    path('vision/', views.vision, name='vision'),
    path('values/', views.values, name='values'),
]
