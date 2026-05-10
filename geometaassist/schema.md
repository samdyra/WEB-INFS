# GeoMetaAssist — Database Schema

Entity-relationship diagram for the GeoMetaAssist Django models.
View this file in VS Code with the Mermaid extension, or paste the
diagram block into https://mermaid.live to render an SVG/PNG.

## ER Diagram

```mermaid
erDiagram
    USER ||--o| USER_SUBSCRIPTION : has
    USER ||--o{ GEO_DATA_PROJECT : owns
    USER ||--o{ AI_CALL_USAGE : performs
    USER ||--o{ METADATA_RECORD : owns

    SUBSCRIPTION_PLAN ||--o{ USER_SUBSCRIPTION : "assigned to"

    GEO_DATA_PROJECT ||--o{ GEOJSON_UPLOAD : contains

    GEOJSON_UPLOAD ||--o| EXTRACTED_TECHNICAL_METADATA : produces
    GEOJSON_UPLOAD ||--o| METADATA_RECORD : has

    USER {
        int id PK
        string email UK
        string first_name
        string last_name
        string password
        bool is_staff
        bool is_superuser
        bool is_active
        datetime date_joined
        datetime last_login
    }

    SUBSCRIPTION_PLAN {
        int id PK
        string name UK
        int max_projects "NULL = unlimited"
        int max_uploads_per_project "NULL = unlimited"
        int max_ai_calls_per_month "NULL = unlimited"
        decimal price_aud
        bool is_active
        datetime created_at
    }

    USER_SUBSCRIPTION {
        int id PK
        int user_id FK "OneToOne -> USER"
        int plan_id FK "-> SUBSCRIPTION_PLAN"
        string status "active | archived"
        date start_date
        date end_date
        datetime archived_at
        int archived_by_id FK "-> USER (nullable)"
        datetime created_at
        datetime updated_at
    }

    AI_CALL_USAGE {
        int id PK
        int user_id FK "-> USER"
        string call_type "suggestion | chat"
        datetime called_at
    }

    GEO_DATA_PROJECT {
        int id PK
        int user_id FK "-> USER"
        string name
        text description
        bool is_deleted
        datetime deleted_at
        datetime created_at
        datetime updated_at
    }

    GEOJSON_UPLOAD {
        int id PK
        int project_id FK "-> GEO_DATA_PROJECT"
        string original_filename
        string file "FileField, UUID-named on disk"
        int file_size_bytes
        string upload_status "pending | processing | complete | error"
        text error_message
        bool is_deleted
        datetime deleted_at
        datetime uploaded_at
        datetime updated_at
    }

    EXTRACTED_TECHNICAL_METADATA {
        int id PK
        int upload_id FK "OneToOne -> GEOJSON_UPLOAD"
        string crs_epsg
        float bbox_minx
        float bbox_miny
        float bbox_maxx
        float bbox_maxy
        string geometry_type
        int feature_count
        json attribute_schema "[{name, dtype}, ...]"
        datetime extracted_at
    }

    METADATA_RECORD {
        int id PK
        int upload_id FK "OneToOne -> GEOJSON_UPLOAD"
        int user_id FK "-> USER"
        string stac_version "default 1.0.0"
        string stac_item_id
        string title
        text description
        json keywords "[string, ...]"
        datetime datetime_start
        datetime datetime_end
        string license "CC-BY-4.0 | CC0-1.0 | OGL-Australia | proprietary | other"
        json providers "[{name, roles}, ...]"
        json links "[{href, rel, title}, ...]"
        json full_stac_json "Final assembled STAC Item"
        bool ai_suggestions_applied
        int export_count
        datetime last_exported_at
        datetime created_at
        datetime updated_at
    }
```

## Relationship summary

| Relationship | Type | From | To |
|---|---|---|---|
| User → UserSubscription | 1:1 (optional) | accounts.User | billing.UserSubscription |
| SubscriptionPlan → UserSubscription | 1:N | billing.SubscriptionPlan | billing.UserSubscription |
| User → AICallUsage | 1:N | accounts.User | billing.AICallUsage |
| User → GeoDataProject | 1:N | accounts.User | projects.GeoDataProject |
| GeoDataProject → GeoJSONUpload | 1:N | projects.GeoDataProject | projects.GeoJSONUpload |
| GeoJSONUpload → ExtractedTechnicalMetadata | 1:1 | projects.GeoJSONUpload | metadata.ExtractedTechnicalMetadata |
| GeoJSONUpload → MetadataRecord | 1:1 | projects.GeoJSONUpload | metadata.MetadataRecord |
| User → MetadataRecord | 1:N | accounts.User | metadata.MetadataRecord |

## Notes

- All foreign keys cascade on delete except `UserSubscription.plan` (PROTECT)
  and `UserSubscription.archived_by` (SET_NULL).
- Soft delete: `GeoDataProject.is_deleted` and `GeoJSONUpload.is_deleted`
  are flags; rows are never hard-deleted in normal flows.
- The actual file content for a `GEOJSON_UPLOAD` lives on disk under
  `MEDIA_ROOT/geojson/<uuid>.geojson` — the `file` column stores the path.
- `ExtractedTechnicalMetadata` and `MetadataRecord` are both created
  automatically by `metadata/extractor.py` once an upload's extraction
  completes, so they exist whenever `upload_status == 'complete'`.
- AI call quota is enforced by counting `AI_CALL_USAGE` rows for the
  current calendar month against `SubscriptionPlan.max_ai_calls_per_month`.
