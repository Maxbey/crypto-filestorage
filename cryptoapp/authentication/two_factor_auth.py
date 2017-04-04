# -*- coding: utf-8 -*-
import six
from authy import AuthyException
from django.conf import settings
from authy.api import AuthyApiClient

from .models import AuthyProfile

AUTHY_KEY = settings.AUTHY_KEY

assert AUTHY_KEY, "You must define a settings.AUTHY['KEY']"

AUTHY_API_URL = 'https://api.authy.com'


class AuthyProvider(object):
    def __init__(self, user):
        self.user = user

        self.errors = {}

        self.client = AuthyApiClient(api_key=AUTHY_KEY, api_uri=AUTHY_API_URL)
        self.force_verification = True

    def make_authy_profile(self, cellphone, authy_id):
        profile, created = AuthyProfile.objects.update_or_create(
            user=self.user,
            defaults={
                'cellphone': cellphone,
                'authy_id': authy_id
            }
        )

        return profile

    def register_user(self, cellphone):
        authy_user = self.client.users.create(
            self.user.username,
            int(cellphone.national_number),
            int(cellphone.country_code)
        )

        if authy_user.ok():
            return self.make_authy_profile(cellphone, authy_user.id)

        errors = authy_user.errors()
        msg = 'Could not register Authy user: %s' % errors
        raise AuthyException(msg)

    def delete_user(self):
        authy_id = self.user.authyprofile.authy_id

        self.client.users.delete(authy_id)

    def verify_token(self, token):
        if not isinstance(token, six.string_types):
            raise AuthyException('Token to validate should be a string.')

        if not token.isdigit():
            raise AuthyException('Token has invalid format.')

        authy_id = int(self.user.authyprofile.authy_id)

        verification = self.client.tokens.verify(
            authy_id, str(token),
            {'force': self.force_verification}
        )

        if verification.ok():
            return True

        self.errors = verification.errors()

        return False
