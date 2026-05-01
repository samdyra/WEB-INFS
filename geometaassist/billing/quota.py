from projects.models import GeoDataProject, GeoJSONUpload

from .models import UserSubscription


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
