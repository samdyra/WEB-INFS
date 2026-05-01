from django.contrib import admin

from .models import SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_projects', 'max_uploads_per_project',
                    'max_ai_calls_per_month', 'price_aud', 'is_active')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'archived_at')
    list_filter = ('plan', 'status')
    search_fields = ('user__email',)
