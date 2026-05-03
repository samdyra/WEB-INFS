from django.conf import settings
from django.db import models


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_projects = models.IntegerField(
        null=True, blank=True, help_text='NULL means unlimited'
    )
    max_uploads_per_project = models.IntegerField(
        null=True, blank=True, help_text='NULL means unlimited'
    )
    max_ai_calls_per_month = models.IntegerField(
        null=True, blank=True, help_text='NULL means unlimited'
    )
    price_aud = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):

    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Active'
        ARCHIVED = 'archived', 'Archived'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription',
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='archived_subscriptions',
    )

    def __str__(self):
        return f'{self.user.email} — {self.plan.name}'

    @property
    def is_pro(self):
        return self.plan.name.lower() == 'pro'


class AICallUsage(models.Model):

    class CallType(models.TextChoices):
        SUGGESTION = 'suggestion', 'Suggestion'
        CHAT       = 'chat',       'Chat'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_calls',
    )
    call_type = models.CharField(max_length=20, choices=CallType.choices)
    called_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-called_at']

    def __str__(self):
        return f'{self.user.email} - {self.call_type} at {self.called_at}'
