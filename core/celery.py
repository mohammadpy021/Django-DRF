from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs automatically.
app.autodiscover_tasks()
