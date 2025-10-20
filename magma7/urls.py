from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('memberships/', include('memberships.urls', namespace='memberships')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('cms/', include('cms.urls', namespace='cms')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls', namespace='users')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
