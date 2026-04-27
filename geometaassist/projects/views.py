from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import GeoDataProjectForm
from .models import GeoDataProject


@login_required
def dashboard(request):
    projects = GeoDataProject.objects.filter(
        user=request.user, is_deleted=False
    ).order_by('-updated_at')
    return render(request, 'projects/dashboard.html', {
        'projects': projects,
        'project_count': projects.count(),
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = GeoDataProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = GeoDataProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        GeoDataProject, pk=pk, user=request.user, is_deleted=False
    )
    return render(request, 'projects/project_detail.html', {'project': project})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(
        GeoDataProject, pk=pk, user=request.user, is_deleted=False
    )
    if request.method == 'POST':
        form = GeoDataProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = GeoDataProjectForm(instance=project)
    return render(request, 'projects/project_edit.html', {
        'form': form,
        'project': project,
    })


@require_POST
@login_required
def project_delete(request, pk):
    project = get_object_or_404(
        GeoDataProject, pk=pk, user=request.user, is_deleted=False
    )
    project.is_deleted = True
    project.deleted_at = timezone.now()
    project.save(update_fields=['is_deleted', 'deleted_at'])
    return redirect('dashboard')
