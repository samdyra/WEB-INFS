from django.contrib import admin

from .models import GeoDataProject


@admin.register(GeoDataProject)
class GeoDataProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'user__email')
