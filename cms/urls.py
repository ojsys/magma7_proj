from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/submit/', views.submit_testimonial, name='submit_testimonial'),
    path('admin/bulk-upload/', views.bulk_upload_media, name='bulk_upload_media'),
    path('admin/ajax-upload/', views.ajax_upload_media, name='ajax_upload_media'),
    # Home gallery bulk upload
    path('admin/home-gallery/bulk-upload/', views.bulk_upload_home_gallery, name='bulk_upload_home_gallery'),
    path('admin/home-gallery/ajax-upload/', views.ajax_upload_home_gallery, name='ajax_upload_home_gallery'),
]
