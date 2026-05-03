import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST

from projects.models import GeoDataProject, GeoJSONUpload

from .extractor import extract_metadata
from .forms import MetadataRecordForm
from .models import MetadataRecord
from .stac_builder import build_stac_item


def _get_user_upload(request, project_pk, upload_pk):
    return get_object_or_404(
        GeoJSONUpload,
        pk=upload_pk,
        project__pk=project_pk,
        project__user=request.user,
        is_deleted=False,
    )


@require_POST
@login_required
def retry_extraction(request, project_pk, upload_pk):
    project = get_object_or_404(
        GeoDataProject, pk=project_pk, user=request.user, is_deleted=False
    )
    upload = get_object_or_404(
        GeoJSONUpload, pk=upload_pk, project=project, is_deleted=False
    )

    if upload.upload_status != GeoJSONUpload.UploadStatus.ERROR:
        messages.warning(request, 'Retry is only available for failed extractions.')
        return redirect('upload_detail', project_pk=project.pk, upload_pk=upload.pk)

    try:
        extract_metadata(upload)
        messages.success(request, 'Extraction completed successfully.')
    except Exception:
        messages.error(request, 'Extraction failed again. See the error message below.')

    return redirect('upload_detail', project_pk=project.pk, upload_pk=upload.pk)


@login_required
@require_http_methods(['GET', 'POST'])
def metadata_editor(request, project_pk, upload_pk):
    upload = _get_user_upload(request, project_pk, upload_pk)

    if upload.upload_status != GeoJSONUpload.UploadStatus.COMPLETE:
        messages.error(request, 'Metadata cannot be edited until extraction is complete.')
        return redirect('upload_detail', project_pk=project_pk, upload_pk=upload_pk)

    record, _ = MetadataRecord.objects.get_or_create(
        upload=upload, defaults={'user': request.user},
    )

    if request.method == 'POST':
        form = MetadataRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Draft saved.')
            return redirect('metadata_editor', project_pk=project_pk, upload_pk=upload_pk)
    else:
        form = MetadataRecordForm(instance=record)

    return render(request, 'metadata/metadata_editor.html', {
        'form': form,
        'upload': upload,
        'project': upload.project,
        'record': record,
        'extracted': upload.extracted_metadata,
    })


@require_POST
@login_required
def export_stac(request, project_pk, upload_pk):
    upload = _get_user_upload(request, project_pk, upload_pk)
    record = get_object_or_404(MetadataRecord, upload=upload)

    record.full_stac_json = build_stac_item(record)
    record.export_count = (record.export_count or 0) + 1
    record.last_exported_at = timezone.now()
    record.save(update_fields=[
        'full_stac_json', 'export_count', 'last_exported_at', 'updated_at',
    ])

    return redirect('export_success', project_pk=project_pk, upload_pk=upload_pk)


@login_required
def export_success(request, project_pk, upload_pk):
    upload = _get_user_upload(request, project_pk, upload_pk)
    record = get_object_or_404(MetadataRecord, upload=upload)

    pretty_json = ''
    if record.full_stac_json is not None:
        pretty_json = json.dumps(record.full_stac_json, indent=2)

    return render(request, 'metadata/export_success.html', {
        'upload': upload,
        'project': upload.project,
        'record': record,
        'pretty_json': pretty_json,
    })


@login_required
def download_stac(request, project_pk, upload_pk):
    upload = _get_user_upload(request, project_pk, upload_pk)
    record = get_object_or_404(MetadataRecord, upload=upload)

    if record.full_stac_json is None:
        messages.error(request, 'No exported STAC JSON yet. Click "Export STAC JSON" first.')
        return redirect('metadata_editor', project_pk=project_pk, upload_pk=upload_pk)

    response = HttpResponse(
        json.dumps(record.full_stac_json, indent=2),
        content_type='application/json',
    )
    filename = f'{record.stac_item_id or upload_pk}_stac.json'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
