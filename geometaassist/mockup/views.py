from django.shortcuts import render


def landing(request):
    return render(request, 'mockup/landing.html')


def login_view(request):
    return render(request, 'mockup/login.html')


def register_view(request):
    return render(request, 'mockup/register.html')


def dashboard(request):
    return render(request, 'mockup/dashboard.html')


def project_create(request):
    return render(request, 'mockup/project_create.html')


def project_detail(request):
    return render(request, 'mockup/project_detail.html')


def project_edit(request):
    return render(request, 'mockup/project_edit.html')


def upload_geojson(request):
    return render(request, 'mockup/upload_geojson.html')


def upload_detail(request):
    return render(request, 'mockup/upload_detail.html')


def metadata_editor(request):
    return render(request, 'mockup/metadata_editor.html')


def export_success(request):
    return render(request, 'mockup/export_success.html')


def admin_subscriptions(request):
    return render(request, 'mockup/admin_subscriptions.html')


def admin_subscription_edit(request):
    return render(request, 'mockup/admin_subscription_edit.html')
