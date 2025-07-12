"""
URL configuration for StackIt project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # API URLs
    path('api/v1/', include('apps.core.api.urls')),
    
    # App URLs
    path('', include('apps.core.urls')),
    path('users/', include('apps.users.urls')),
    path('questions/', include('apps.questions.urls')),
    path('answers/', include('apps.answers.urls')),
    path('notifications/', include('apps.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
