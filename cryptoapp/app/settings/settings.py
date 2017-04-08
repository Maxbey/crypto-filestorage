from django.utils.crypto import get_random_string
from configurations import values

from .base import BaseSettings


class Development(BaseSettings):
    DEBUG = True
    SECRET_KEY = get_random_string(length=32)

    DATABASES = values.DatabaseURLValue(
        environ_required=True,
        environ_prefix='',
        environ_name='DATABASE_URL'
    )

    AUTHY_KEY = values.SecretValue(
        environ_required=True,
        environ_prefix=''
    )

    ENC_KEY = values.SecretValue(
        environ_required=True,
        environ_prefix=''
    )


class Test(BaseSettings):
    DEBUG = True
    SECRET_KEY = get_random_string(length=32)
    AUTHY_KEY = 'key'

    INSTALLED_APPS = BaseSettings.INSTALLED_APPS + [
        'django_extensions'
    ]