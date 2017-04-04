from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class Test(APITestCase):
    url = '/api/auth/login/'

    def test_test(self):
        user = User.objects.create(
            username='email@email.com',
            email='email@email.com'
        )
        user.set_password('passpass')
        user.save()

        payload = {
            'username': 'email@email.com',
            'password': 'passpass'
        }

        response = self.client.post(self.url, data=payload)
        import pudb; pu.db
        a = ''