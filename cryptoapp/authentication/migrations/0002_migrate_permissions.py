# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def migrate_permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(
        User
    )

    permission = Permission.objects.create(
        codename='permissions_manage_access',
        name='Can manage user permissions',
        content_type=content_type
    )

    support_group = Group.objects.create(name='moderators')
    support_group.permissions.add(permission)


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_permissions)
    ]
