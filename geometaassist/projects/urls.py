from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:project_pk>/upload/', views.upload_geojson, name='upload_geojson'),
    path('<int:project_pk>/uploads/<int:upload_pk>/', views.upload_detail, name='upload_detail'),
    path('<int:project_pk>/uploads/<int:upload_pk>/delete/', views.upload_delete, name='upload_delete'),
]
