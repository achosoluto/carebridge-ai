"""Celery configuration for CareBridge AI."""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('carebridge_ai')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery configuration options
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Only accept JSON in tasks
    result_serializer='json',
    timezone='America/Edmonton',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=20 * 60,  # 20 minutes
    worker_max_tasks_per_child=1000,
)