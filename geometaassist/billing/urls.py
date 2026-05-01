from django.urls import path

from . import views

urlpatterns = [
    path('billing/quota-exceeded/', views.quota_exceeded, name='quota_exceeded'),
    path('billing/upgrade/', views.upgrade_to_pro, name='upgrade_to_pro'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/subscriptions/', views.staff_subscriptions, name='staff_subscriptions'),
    path('staff/subscriptions/<int:pk>/edit/', views.staff_subscription_edit, name='staff_subscription_edit'),
]
