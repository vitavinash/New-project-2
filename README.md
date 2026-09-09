# SmartEye eQMS Django Website

Professional Django website for SmartEye eQMS with animated frontend graphics, a PostgreSQL-backed consultation form, and Django admin lead management.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a local PostgreSQL database:

```sql
CREATE DATABASE smarteye_eqms;
```

4. Update `.env` with your PostgreSQL username, password, host, and database name.
5. Run migrations:

```bash
python manage.py migrate
```

6. Create an admin user:

```bash
python manage.py createsuperuser
```

7. Start the server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Features

- Animated, responsive product homepage for SmartEye eQMS.
- PostgreSQL database configuration through `.env`.
- Functional demo/contact form.
- Lead storage and search in Django admin.
- Production-friendly static file setup with WhiteNoise.
- Responsive visual design with laboratory photography, light/dark themes, and mobile navigation.
- Searchable sample traceability matrix with record inspection and CSV export.
- Interactive device-category tabs and time-savings calculator.
- Personal action workspace with persistent records, priorities, due dates, status updates, filtering, and CSV export.

## Verification

```bash
python manage.py test website --noinput
```

Existing installations should run `python manage.py migrate` to add the action-item table. Sign in using an existing Django username and password to access the workspace.

See [PROJECT.md](PROJECT.md) for routes, implementation details, and the distinction between sample traceability data and persisted personal actions.
