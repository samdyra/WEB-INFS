from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/1/', views.project_detail, name='project_detail'),
    path('projects/1/edit/', views.project_edit, name='project_edit'),
    path('projects/1/upload/', views.upload_geojson, name='upload_geojson'),
    path('projects/1/uploads/1/', views.upload_detail, name='upload_detail'),
    path('projects/1/uploads/1/metadata/', views.metadata_editor, name='metadata_editor'),
    path('projects/1/uploads/1/export/', views.export_success, name='export_success'),
    path('admin-portal/subscriptions/', views.admin_subscriptions, name='admin_subscriptions'),
    path('admin-portal/subscriptions/1/edit/', views.admin_subscription_edit, name='admin_subscription_edit'),
]
