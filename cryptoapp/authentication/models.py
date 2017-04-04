from __future__ import unicode_literals
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class AuthyProfile(models.Model):
    user = models.OneToOneField('auth.User')
    authy_id = models.CharField(max_length=64, null=True, db_index=True)
    cellphone = PhoneNumberField(db_index=True, null=True)


