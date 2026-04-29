import os
import uuid

from django.conf import settings
from django.db import models


def geojson_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'geojson/{uuid.uuid4().hex}{ext}'


class GeoDataProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class GeoJSONUpload(models.Model):

    class UploadStatus(models.TextChoices):
        PENDING    = 'pending',    'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETE   = 'complete',   'Complete'
        ERROR      = 'error',      'Error'

    project = models.ForeignKey(
        GeoDataProject, on_delete=models.CASCADE, related_name='uploads'
    )
    original_filename = models.CharField(max_length=255)
    file = models.FileField(upload_to=geojson_upload_path)
    file_size_bytes = models.IntegerField(null=True, blank=True)
    upload_status = models.CharField(
        max_length=20,
        choices=UploadStatus.choices,
        default=UploadStatus.PENDING,
    )
    error_message = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.original_filename

    def status_badge_class(self):
        return {
            self.UploadStatus.COMPLETE:   'bg-success',
            self.UploadStatus.PROCESSING: 'bg-warning text-dark',
            self.UploadStatus.PENDING:    'bg-secondary',
            self.UploadStatus.ERROR:      'bg-danger',
        }.get(self.upload_status, 'bg-secondary')
