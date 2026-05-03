from django.contrib import admin

from .models import ExtractedTechnicalMetadata, MetadataRecord


@admin.register(ExtractedTechnicalMetadata)
class ExtractedTechnicalMetadataAdmin(admin.ModelAdmin):
    list_display = ('upload', 'crs_epsg', 'geometry_type', 'feature_count', 'extracted_at')
    search_fields = ('upload__original_filename', 'upload__project__name')


@admin.register(MetadataRecord)
class MetadataRecordAdmin(admin.ModelAdmin):
    list_display = ('upload', 'user', 'title', 'license',
                    'export_count', 'last_exported_at', 'ai_suggestions_applied')
    list_filter = ('license', 'ai_suggestions_applied')
    search_fields = ('title', 'stac_item_id', 'upload__original_filename', 'user__email')
