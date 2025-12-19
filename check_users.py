#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatboard.settings')
django.setup()

from django.contrib.auth.models import User

print('All users in database:')
for user in User.objects.all():
    print(f'  - {user.username} ({user.email})')
