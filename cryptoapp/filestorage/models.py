from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import models


class File(models.Model):
    user = models.ForeignKey('auth.User')

    name = models.CharField(max_length=255)
    content = models.TextField()

    original_content_length = models.PositiveSmallIntegerField(default=0)
    groups = models.ManyToManyField(Group, related_name='files')
