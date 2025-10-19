from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/submit/', views.submit_testimonial, name='submit_testimonial'),
]

