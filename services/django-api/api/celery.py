import os
from celery import Celery

# Tell Celery where Django settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

# Create Celery app
app = Celery("api")

# Load settings from Django settings.py (CELERY_*)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py in all INSTALLED_APPS
app.autodiscover_tasks()
