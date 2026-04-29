from django.contrib import admin

from .models import GeoDataProject, GeoJSONUpload


@admin.register(GeoDataProject)
class GeoDataProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'user__email')


@admin.register(GeoJSONUpload)
class GeoJSONUploadAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'project', 'upload_status',
                    'file_size_bytes', 'uploaded_at', 'is_deleted')
    list_filter = ('upload_status', 'is_deleted')
    search_fields = ('original_filename', 'project__name')
