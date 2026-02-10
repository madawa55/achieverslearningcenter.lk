"""
URL configuration for Achievers Learning Center
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core import views as core_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Core pages
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),

    # Courses
    path('courses/', include('apps.courses.urls')),

    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),

    # Attendance
    path('attendance/', include('apps.attendance.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
