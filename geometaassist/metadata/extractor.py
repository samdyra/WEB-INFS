import geopandas as gpd


def extract_metadata(upload):
    """
    Read the uploaded GeoJSON file with GeoPandas and store technical
    metadata. Updates upload.upload_status throughout. Sets ERROR
    on failure and re-raises.
    """
    from projects.models import GeoJSONUpload

    from .models import ExtractedTechnicalMetadata, MetadataRecord

    upload.upload_status = GeoJSONUpload.UploadStatus.PROCESSING
    upload.save(update_fields=['upload_status', 'updated_at'])

    try:
        gdf = gpd.read_file(upload.file.path)

        crs_epsg = ''
        if gdf.crs is not None:
            epsg = gdf.crs.to_epsg()
            crs_epsg = f'EPSG:{epsg}' if epsg else str(gdf.crs)

        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

        geom_types = gdf.geom_type.dropna().unique().tolist()
        geometry_type = ', '.join(geom_types) if geom_types else 'Unknown'

        feature_count = len(gdf)

        attribute_schema = [
            {'name': col, 'dtype': str(gdf[col].dtype)}
            for col in gdf.columns
            if col != gdf.geometry.name
        ]

        meta, _ = ExtractedTechnicalMetadata.objects.update_or_create(
            upload=upload,
            defaults={
                'crs_epsg':         crs_epsg,
                'bbox_minx':        float(bounds[0]),
                'bbox_miny':        float(bounds[1]),
                'bbox_maxx':        float(bounds[2]),
                'bbox_maxy':        float(bounds[3]),
                'geometry_type':    geometry_type,
                'feature_count':    feature_count,
                'attribute_schema': attribute_schema,
            },
        )

        upload.upload_status = GeoJSONUpload.UploadStatus.COMPLETE
        upload.error_message = ''
        upload.save(update_fields=['upload_status', 'error_message', 'updated_at'])

        MetadataRecord.objects.get_or_create(
            upload=upload,
            defaults={'user': upload.project.user},
        )

        return meta

    except Exception as e:
        upload.upload_status = GeoJSONUpload.UploadStatus.ERROR
        upload.error_message = str(e)
        upload.save(update_fields=['upload_status', 'error_message', 'updated_at'])
        raise
