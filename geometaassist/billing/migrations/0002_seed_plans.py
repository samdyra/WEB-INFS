from django.db import migrations


def seed_plans_and_backfill(apps, schema_editor):
    SubscriptionPlan = apps.get_model('billing', 'SubscriptionPlan')
    UserSubscription = apps.get_model('billing', 'UserSubscription')
    User = apps.get_model('accounts', 'User')

    free, _ = SubscriptionPlan.objects.get_or_create(
        name='Free',
        defaults={
            'max_projects': 2,
            'max_uploads_per_project': 5,
            'max_ai_calls_per_month': 10,
            'price_aud': 0,
        },
    )
    SubscriptionPlan.objects.get_or_create(
        name='Pro',
        defaults={
            'max_projects': None,
            'max_uploads_per_project': None,
            'max_ai_calls_per_month': None,
            'price_aud': 29,
        },
    )

    for user in User.objects.filter(subscription__isnull=True):
        UserSubscription.objects.create(user=user, plan=free)


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_plans_and_backfill, reverse_noop),
    ]
