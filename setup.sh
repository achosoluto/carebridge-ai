#!/bin/bash
cd backend
python manage.py migrate --settings=carebridge.settings_test
python manage.py createsuperuser --noinput --username testuser --email test@example.com --settings=carebridge.settings_test
# Set password and permissions programmatically
python manage.py shell --settings=carebridge.settings_test -c "
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='testuser')
u.set_password('testpass')
u.is_staff = True
u.is_superuser = True
u.save()
"