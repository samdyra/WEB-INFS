from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .decorators import staff_required
from .forms import StaffSubscriptionForm
from .models import SubscriptionPlan, UserSubscription


@login_required
def quota_exceeded(request):
    quota_type = request.GET.get('type', 'project')
    if quota_type not in ('project', 'upload'):
        quota_type = 'project'
    subscription = UserSubscription.objects.filter(
        user=request.user
    ).select_related('plan').first()
    pro_plan = SubscriptionPlan.objects.filter(name='Pro').first()
    return render(request, 'billing/quota_exceeded.html', {
        'quota_type': quota_type,
        'subscription': subscription,
        'pro_plan': pro_plan,
    })


@require_POST
@login_required
def upgrade_to_pro(request):
    subscription = get_object_or_404(UserSubscription, user=request.user)
    pro_plan = get_object_or_404(SubscriptionPlan, name='Pro')
    subscription.plan = pro_plan
    subscription.status = UserSubscription.Status.ACTIVE
    subscription.archived_at = None
    subscription.archived_by = None
    subscription.save()
    return JsonResponse({'success': True, 'plan': pro_plan.name})


@staff_required
def staff_dashboard(request):
    return redirect('staff_subscriptions')


@staff_required
def staff_subscriptions(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', 'all')

    qs = UserSubscription.objects.select_related(
        'user', 'plan').order_by('-created_at')
    if q:
        qs = qs.filter(user__email__icontains=q)
    if status in ('active', 'archived'):
        qs = qs.filter(status=status)

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'billing/staff_subscriptions.html', {
        'page_obj': page_obj,
        'subscriptions': page_obj.object_list,
        'total_count': paginator.count,
        'q': q,
        'status_filter': status,
    })


@staff_required
def staff_subscription_edit(request, pk):
    subscription = get_object_or_404(UserSubscription, pk=pk)
    previous_status = subscription.status
    if request.method == 'POST':
        form = StaffSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            sub = form.save(commit=False)
            if sub.status == UserSubscription.Status.ARCHIVED and previous_status != UserSubscription.Status.ARCHIVED:
                sub.archived_at = timezone.now()
                sub.archived_by = request.user
            elif sub.status == UserSubscription.Status.ACTIVE and previous_status == UserSubscription.Status.ARCHIVED:
                sub.archived_at = None
                sub.archived_by = None
            sub.save()
            messages.success(request, 'Subscription updated successfully.')
            return redirect('staff_subscriptions')
    else:
        form = StaffSubscriptionForm(instance=subscription)
    return render(request, 'billing/staff_subscription_edit.html', {
        'form': form,
        'subscription': subscription,
    })
