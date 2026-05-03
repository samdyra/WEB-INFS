def build_stac_item(record):
    """Assemble a STAC 1.0.0 Item dict from a MetadataRecord."""
    upload = record.upload
    meta = upload.extracted_metadata

    bbox = [meta.bbox_minx, meta.bbox_miny, meta.bbox_maxx, meta.bbox_maxy]

    minx, miny, maxx, maxy = bbox
    geometry = {
        'type': 'Polygon',
        'coordinates': [[
            [minx, miny], [maxx, miny],
            [maxx, maxy], [minx, maxy],
            [minx, miny],
        ]],
    }

    properties = {
        'title':       record.title,
        'description': record.description,
        'license':     record.license,
    }
    if record.datetime_start and record.datetime_end:
        properties['datetime'] = None
        properties['start_datetime'] = record.datetime_start.isoformat()
        properties['end_datetime'] = record.datetime_end.isoformat()
    elif record.datetime_start:
        properties['datetime'] = record.datetime_start.isoformat()
    else:
        properties['datetime'] = None

    if record.keywords:
        properties['keywords'] = record.keywords

    return {
        'type':         'Feature',
        'stac_version': record.stac_version,
        'id':           record.stac_item_id or str(upload.pk),
        'geometry':     geometry,
        'bbox':         bbox,
        'properties':   properties,
        'links':        record.links or [],
        'assets': {
            'data': {
                'href':  upload.original_filename,
                'type':  'application/geo+json',
                'title': record.title or upload.original_filename,
            },
        },
        'providers': record.providers or [],
    }
