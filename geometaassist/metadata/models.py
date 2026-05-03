from django.conf import settings
from django.db import models


class ExtractedTechnicalMetadata(models.Model):
    upload = models.OneToOneField(
        'projects.GeoJSONUpload',
        on_delete=models.CASCADE,
        related_name='extracted_metadata',
    )
    crs_epsg = models.CharField(max_length=50, blank=True)
    bbox_minx = models.FloatField(null=True, blank=True)
    bbox_miny = models.FloatField(null=True, blank=True)
    bbox_maxx = models.FloatField(null=True, blank=True)
    bbox_maxy = models.FloatField(null=True, blank=True)
    geometry_type = models.CharField(max_length=50, blank=True)
    feature_count = models.IntegerField(null=True, blank=True)
    attribute_schema = models.JSONField(
        default=list,
        help_text='Array of {name, dtype} objects',
    )
    extracted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Metadata for {self.upload.original_filename}'

    @property
    def bbox_display(self):
        if None in (self.bbox_minx, self.bbox_miny,
                    self.bbox_maxx, self.bbox_maxy):
            return 'N/A'
        return (f'{self.bbox_minx:.4f}, {self.bbox_miny:.4f}, '
                f'{self.bbox_maxx:.4f}, {self.bbox_maxy:.4f}')


class MetadataRecord(models.Model):

    LICENSE_CHOICES = [
        ('CC-BY-4.0',     'CC-BY-4.0 (Attribution)'),
        ('CC-BY-SA-4.0',  'CC-BY-SA-4.0 (Attribution-ShareAlike)'),
        ('CC0-1.0',       'CC0-1.0 (Public Domain)'),
        ('OGL-Australia', 'OGL Australia (Open Government Licence)'),
        ('proprietary',   'Proprietary'),
        ('other',         'Other'),
    ]

    upload = models.OneToOneField(
        'projects.GeoJSONUpload',
        on_delete=models.CASCADE,
        related_name='metadata_record',
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stac_version = models.CharField(max_length=10, default='1.0.0')
    stac_item_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    keywords = models.JSONField(default=list, help_text='Stored as array of strings')
    datetime_start = models.DateTimeField(null=True, blank=True)
    datetime_end = models.DateTimeField(null=True, blank=True)
    license = models.CharField(max_length=50, blank=True, choices=LICENSE_CHOICES)
    providers = models.JSONField(default=list, help_text='Array of STAC provider objects')
    links = models.JSONField(default=list, help_text='Array of STAC link objects')
    full_stac_json = models.JSONField(
        null=True, blank=True, help_text='Final assembled STAC Item'
    )
    ai_suggestions_applied = models.BooleanField(default=False)
    export_count = models.IntegerField(default=0)
    last_exported_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.title or self.stac_item_id
                or f'Record for {self.upload.original_filename}')
