
How to run this Project: 

1. Create and activate a virtual environment
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Run database migrations
python manage.py migrate

4. Start the development server
python manage.py runserver

The app will be available at `http://127.0.0.1:8000/` (by default).

## Pages & Routes

| #  | Page                        | Template File                  | Route                                    | View Function                |
|----|-----------------------------|--------------------------------|------------------------------------------|------------------------------|
| 1  | Base layout (authenticated) | `base.html`                    | *(layout only — no route)*               | —                            |
| 2  | Base layout (public)        | `base_public.html`             | *(layout only — no route)*               | —                            |
| 3  | Landing page                | `landing.html`                 | `/`                                      | `landing()`                  |
| 4  | Login                       | `login.html`                   | `/accounts/login/`                       | `login_view()`               |
| 5  | Register                    | `register.html`                | `/accounts/register/`                    | `register_view()`            |
| 6  | Dashboard                   | `dashboard.html`               | `/dashboard/`                            | `dashboard()`                |
| 7  | Create project              | `project_create.html`          | `/projects/create/`                      | `project_create()`           |
| 8  | Edit project                | `project_edit.html`            | `/projects/<id>/edit/`                   | `project_edit()`             |
| 9  | Project detail              | `project_detail.html`          | `/projects/<id>/`                        | `project_detail()`           |
| 10 | Upload GeoJSON              | `upload_geojson.html`          | `/projects/<id>/upload/`                 | `upload_geojson()`           |
| 11 | Upload detail               | `upload_detail.html`           | `/projects/<id>/uploads/<id>/`           | `upload_detail()`            |
| 12 | Metadata editor             | `metadata_editor.html`         | `/projects/<id>/uploads/<id>/metadata/`  | `metadata_editor()`          |
| 13 | Export success              | `export_success.html`          | `/projects/<id>/uploads/<id>/export/`    | `export_success()`           |
| 14 | Admin subscriptions         | `admin_subscriptions.html`     | `/admin-portal/subscriptions/`           | `admin_subscriptions()`      |
| 15 | Admin subscription edit     | `admin_subscription_edit.html` | `/admin-portal/subscriptions/<id>/edit/` | `admin_subscription_edit()`  |

All views are defined in `mockup/views.py` and routes in `mockup/urls.py`.


how to ingest: python manage.py ingest_stac_spec

AI Usage