# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from filestorage.models import File


def migrate_permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(
        File
    )

    Permission.objects.create(
        codename='view_file',
        name='Can view file',
        content_type=content_type
    )
    Permission.objects.create(
        codename='decrypt_file',
        name='Can decrypt file',
        content_type=content_type
    )


class Migration(migrations.Migration):
    dependencies = [
        ('filestorage', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_permissions)
    ]
