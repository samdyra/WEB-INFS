from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from billing.models import SubscriptionPlan, UserSubscription

from .forms import LoginForm, PasswordChangeForm, ProfileForm, RegisterForm


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    free_plan = SubscriptionPlan.objects.filter(name='Free').first()
    pro_plan = SubscriptionPlan.objects.filter(name='Pro').first()
    return render(request, 'landing.html', {
        'free_plan': free_plan,
        'pro_plan':  pro_plan,
    })


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            free_plan = SubscriptionPlan.objects.get(name='Free')
            UserSubscription.objects.create(user=user, plan=free_plan)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('dashboard')
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated.')
                return redirect('profile')
        elif action == 'change_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password updated.')
                return redirect('profile')

    return render(request, 'accounts/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })
