from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    projects_qs = GeoDataProject.objects.filter(
        user=request.user, is_deleted=False
    ).order_by('-updated_at')
    total_uploads = GeoJSONUpload.objects.filter(
        project__user=request.user,
        project__is_deleted=False,
        is_deleted=False,
    ).count()

    paginator = Paginator(projects_qs, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'projects/dashboard.html', {
        'projects':      page.object_list,
        'page':          page,
        'project_count': projects_qs.count(),
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
            messages.success(request, 'Project created successfully.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = GeoDataProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        GeoDataProject, pk=pk, user=request.user, is_deleted=False
    )
    uploads_qs = project.uploads.filter(is_deleted=False).order_by('-uploaded_at')

    paginator = Paginator(uploads_qs, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'projects/project_detail.html', {
        'project':      project,
        'uploads':      page.object_list,
        'page':         page,
        'upload_count': uploads_qs.count(),
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
            messages.success(request, 'Project updated successfully.')
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
    messages.success(request, 'Project deleted.')
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
                messages.success(request, 'File uploaded and extraction complete.')
            except Exception:
                messages.warning(
                    request,
                    'File uploaded but extraction failed. '
                    'You can retry from the upload detail page.',
                )
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
    record = getattr(upload, 'metadata_record', None)
    return render(request, 'projects/upload_detail.html', {
        'project': project,
        'upload':  upload,
        'record':  record,
    })


@login_required
def upload_history(request):
    base_qs = GeoJSONUpload.objects.filter(
        project__user=request.user,
        project__is_deleted=False,
        is_deleted=False,
    ).select_related('project').order_by('-uploaded_at')

    total_count = base_qs.count()
    complete_count = base_qs.filter(
        upload_status=GeoJSONUpload.UploadStatus.COMPLETE,
    ).count()
    error_count = base_qs.filter(
        upload_status=GeoJSONUpload.UploadStatus.ERROR,
    ).count()

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    uploads = base_qs
    if q:
        uploads = uploads.filter(original_filename__icontains=q)
    if status and status in GeoJSONUpload.UploadStatus.values:
        uploads = uploads.filter(upload_status=status)

    paginator = Paginator(uploads, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'projects/upload_history.html', {
        'page':           page,
        'uploads':        page.object_list,
        'total_count':    total_count,
        'complete_count': complete_count,
        'error_count':    error_count,
        'q':              q,
        'status':         status,
        'status_choices': GeoJSONUpload.UploadStatus.choices,
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
    messages.success(request, 'Upload deleted.')
    return redirect('project_detail', pk=project.pk)
