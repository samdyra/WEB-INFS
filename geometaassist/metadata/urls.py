from django.urls import path

from . import views

urlpatterns = [
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/retry/',
        views.retry_extraction,
        name='retry_extraction',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/metadata_editor/',
        views.metadata_editor,
        name='metadata_editor',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/export/',
        views.export_stac,
        name='export_stac',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/export_success/',
        views.export_success,
        name='export_success',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/download/',
        views.download_stac,
        name='download_stac',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/ai-suggest/',
        views.ai_suggest,
        name='ai_suggest',
    ),
    path(
        'metadata/<int:project_pk>/uploads/<int:upload_pk>/ai-chat/',
        views.ai_chat,
        name='ai_chat',
    ),
]
