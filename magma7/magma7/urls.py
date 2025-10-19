from django.contrib import admin
from django.urls import path, include

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
