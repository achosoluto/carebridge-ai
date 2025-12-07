#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        password='password',
        email='admin@example.com'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Collect static files (for production)
python manage.py collectstatic --noinput

# Start the server with gunicorn
exec gunicorn carebridge.wsgi:application --bind 0.0.0.0:8000 --workers 3