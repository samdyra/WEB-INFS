from django.utils import timezone

from projects.models import GeoDataProject, GeoJSONUpload

from .models import AICallUsage, UserSubscription


def _get_subscription(user):
    return UserSubscription.objects.filter(user=user).select_related('plan').first()


def can_create_project(user):
    sub = _get_subscription(user)
    if sub is None:
        return True, None
    limit = sub.plan.max_projects
    if limit is None:
        return True, None
    current = GeoDataProject.objects.filter(user=user, is_deleted=False).count()
    if current >= limit:
        return False, limit
    return True, None


def can_upload_file(user, project):
    sub = _get_subscription(user)
    if sub is None:
        return True, None
    limit = sub.plan.max_uploads_per_project
    if limit is None:
        return True, None
    current = GeoJSONUpload.objects.filter(project=project, is_deleted=False).count()
    if current >= limit:
        return False, limit
    return True, None


def can_use_ai(user):
    sub = _get_subscription(user)
    if sub is None:
        return False, 'No active subscription.'

    limit = sub.plan.max_ai_calls_per_month
    if limit is None:
        return True, None

    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    used = AICallUsage.objects.filter(user=user, called_at__gte=month_start).count()

    if used >= limit:
        return False, (
            f'You have used {used} of {limit} AI calls this month. '
            'Upgrade to Pro for unlimited calls.'
        )
    return True, None


def record_ai_call(user, call_type):
    AICallUsage.objects.create(user=user, call_type=call_type)
