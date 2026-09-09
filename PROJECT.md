# SmartEye eQMS Project

SmartEye eQMS is a Django website presenting a quality management platform for medical device teams. The project includes a product homepage, a consultation form, user login, a protected workspace, and lead management through Django admin.

## Current Functionality

- The homepage presents product modules, regulatory frameworks, integrations, and sample traceability records.
- Valid consultation submissions are saved to the database and redirect to a thank-you page.
- Existing Django users can sign in and access the workspace.
- Administrators can search leads and filter them by company size and creation date.
- The workspace stores personal action items in the database, with priorities, due dates, status updates, search, filters, and CSV export. Metrics reflect the signed-in user's saved actions.
- The homepage provides searchable sample traceability records, record inspection, CSV download, device-category tabs, and a time-savings calculator.
- Shared navigation supports mobile screens and a saved light/dark theme preference.

Product descriptions of integrations, signatures, risk management, and compliance are presentation content. They do not establish implemented integrations or validated compliance workflows in this codebase.

## Technology

| Component | Implementation |
| --- | --- |
| Backend | Django 5.1.4 |
| Frontend | Django templates, responsive CSS, vanilla JavaScript, and locally served Lucide icons |
| Database | PostgreSQL, with database URL configuration and a serverless SQLite fallback |
| Authentication | Django authentication and sessions |
| Configuration | python-decouple and dj-database-url |
| Static assets | WhiteNoise |
| Deployment configuration | Vercel Python entry point |

## Project Structure

```text
api/index.py           Vercel entry point
smarteye/settings.py    Django settings and database configuration
smarteye/urls.py        Root routes and admin registration
website/models.py      Consultation leads and user-owned action items
website/forms.py       Lead form and validation
website/views.py       Page handlers, action management, and sample trace data
website/urls.py        Website routes
website/admin.py       Lead administration
website/migrations/    Database migrations
templates/website/     Page templates
static/css/            Source stylesheets
static/js/             Site interactions and bundled Lucide icons
static/images/         Laboratory image and source credit
staticfiles/           Collected static assets
manage.py              Django management entry point
requirements.txt       Python dependencies
vercel.json            Vercel build and routing configuration
.env.example           Example local settings
```

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Product homepage and consultation form |
| `/thanks/` | Consultation confirmation |
| `/login/` | Sign in with Django credentials |
| `/logout/` | POST to end the session and return home |
| `/workspace/` | Authenticated personal actions, filters, metrics, and CSV export |
| `/workspace/actions/<id>/status/` | POST a status update for an action owned by the signed-in user |
| `/admin/` | Django administration for authorized staff |

## Local Setup

Install Python and PostgreSQL before starting. From the project directory, create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a PostgreSQL database named `smarteye_eqms`. For a new checkout, create `.env` using `.env.example` as a reference. If `.env` already exists, update its values as needed.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key; set a unique value for deployment |
| `DEBUG` | Enable locally; set to `False` for production |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | Optional database connection URL; takes precedence over PostgreSQL fields |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_HOST` | Database host |
| `POSTGRES_PORT` | Database port, normally `5432` |

Initialize the database and start Django:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. The created superuser can access both the workspace and Django admin. The login handler authenticates using the Django username.

## Lead Data

Consultation records require a name, email, and company. Optional fields include phone, company size, interest, and message. Django records the creation time automatically and lists the newest leads first.

## Deployment Notes

`vercel.json` routes requests through `api/index.py` and configures `python manage.py collectstatic --noinput` as the build command. Configure the deployment environment and run database migrations against the target database before using database-backed features.

Use a persistent database for retained leads and user accounts. The serverless SQLite fallback uses `/tmp/db.sqlite3`, which is temporary storage.

## Manual Verification

1. Run `python manage.py check` after configuring the environment.
2. Load the homepage and submit a valid consultation form.
3. Confirm the redirect to `/thanks/` and the saved record in Django admin.
4. Submit an invalid email and confirm form validation prevents saving.
5. Visit `/workspace/` while signed out and confirm redirection to login.
6. Sign in, create an action, change its status, and verify that filters and metrics update.
7. Export the filtered action list, then sign out.
8. Search the homepage traceability sample and download its CSV.
9. Test the device tabs, time-savings calculator, mobile navigation, and theme control.

## Automated Tests

Run `python manage.py test website --noinput`. The suite covers consultation validation, page rendering, authentication, action ownership, filtering, metrics, CSV escaping, and CSRF protection. Django creates a separate test database, so the configured database user must have permission to create it.

The action queue is a personal task tracker. It does not implement regulated electronic signatures or controlled quality-record approvals. Homepage traceability records remain illustrative.

See [README.md](README.md) for the original quick-start guide.
