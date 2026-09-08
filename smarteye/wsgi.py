import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smarteye.settings")

application = get_wsgi_application()

# Vercel serverless Python runtime looks for 'app' handler
app = application

# Auto-migrate on Vercel serverless if needed
if os.environ.get("VERCEL"):
    try:
        from django.core.management import call_command
        call_command("migrate", interactive=False)
    except Exception as exc:
        print(f"Startup migration notice: {exc}")

