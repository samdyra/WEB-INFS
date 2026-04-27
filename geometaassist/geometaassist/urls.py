from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from accounts import views as account_views
from projects import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.landing_view, name='landing'),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', project_views.dashboard, name='dashboard'),
    path('projects/', include('projects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
