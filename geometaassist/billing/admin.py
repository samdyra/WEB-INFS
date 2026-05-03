from django.contrib import admin

from .models import AICallUsage, SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_projects', 'max_uploads_per_project',
                    'max_ai_calls_per_month', 'price_aud', 'is_active')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'archived_at')
    list_filter = ('plan', 'status')
    search_fields = ('user__email',)


@admin.register(AICallUsage)
class AICallUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'call_type', 'called_at')
    list_filter = ('call_type',)
    search_fields = ('user__email',)
    date_hierarchy = 'called_at'
