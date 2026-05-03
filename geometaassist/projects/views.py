from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from billing.quota import can_create_project, can_upload_file
from metadata.extractor import extract_metadata

from .forms import GeoDataProjectForm, GeoJSONUploadForm
from .models import GeoDataProject, GeoJSONUpload


@login_required
def dashboard(request):
    projects = GeoDataProject.objects.filter(
        user=request.user, is_deleted=False
    ).order_by('-updated_at')
    total_uploads = GeoJSONUpload.objects.filter(
        project__user=request.user,
        project__is_deleted=False,
        is_deleted=False,
    ).count()
    return render(request, 'projects/dashboard.html', {
        'projects': projects,
        'project_count': projects.count(),
        'total_uploads': total_uploads,
    })


@login_required
def project_create(request):
    allowed, _ = can_create_project(request.user)
    if not allowed:
        return redirect(f"{reverse('quota_exceeded')}?type=project")
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
    uploads = project.uploads.filter(is_deleted=False).order_by('-uploaded_at')
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'uploads': uploads,
        'upload_count': uploads.count(),
    })


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


@login_required
def upload_geojson(request, project_pk):
    project = get_object_or_404(
        GeoDataProject, pk=project_pk, user=request.user, is_deleted=False
    )
    allowed, _ = can_upload_file(request.user, project)
    if not allowed:
        return redirect(f"{reverse('quota_exceeded')}?type=upload")
    if request.method == 'POST':
        form = GeoJSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            upload = GeoJSONUpload.objects.create(
                project=project,
                original_filename=f.name,
                file=f,
                file_size_bytes=f.size,
                upload_status=GeoJSONUpload.UploadStatus.PENDING,
            )
            try:
                extract_metadata(upload)
            except Exception:
                pass  # Error is recorded on the upload; user sees it on detail page.
            return redirect('upload_detail', project_pk=project.pk, upload_pk=upload.pk)
    else:
        form = GeoJSONUploadForm()
    return render(request, 'projects/upload_geojson.html', {
        'project': project,
        'form': form,
    })


@login_required
def upload_detail(request, project_pk, upload_pk):
    project = get_object_or_404(
        GeoDataProject, pk=project_pk, user=request.user, is_deleted=False
    )
    upload = get_object_or_404(
        GeoJSONUpload, pk=upload_pk, project=project, is_deleted=False
    )
    return render(request, 'projects/upload_detail.html', {
        'project': project,
        'upload': upload,
    })


@require_POST
@login_required
def upload_delete(request, project_pk, upload_pk):
    project = get_object_or_404(
        GeoDataProject, pk=project_pk, user=request.user, is_deleted=False
    )
    upload = get_object_or_404(
        GeoJSONUpload, pk=upload_pk, project=project, is_deleted=False
    )
    upload.is_deleted = True
    upload.deleted_at = timezone.now()
    upload.save(update_fields=['is_deleted', 'deleted_at'])
    return redirect('project_detail', pk=project.pk)
