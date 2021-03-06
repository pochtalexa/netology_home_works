# Generated by Django 3.1.2 on 2021-06-01 16:39

from django.db import migrations, models
from django.contrib.auth.models import User
import datetime


def add_admin(app, schema_editor):
    user = User(
        id=1,
        username='admin',
        is_active=True,
        email='admin@email.com',
        is_staff=True,
        is_superuser=True,
        last_login=datetime.datetime.now()
    )
    user.set_password('admin')
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0002_auto_20210601_1937'),
    ]

    operations = [
        migrations.RunPython(add_admin)
    ]
