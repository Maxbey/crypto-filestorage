from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class Test(APITestCase):
    url = '/api/auth/group/'

    def test_test(self):
        user = User.objects.create(
            username='email@email.com',
            email='email@email.com'
        )

        token = Token.objects.create(user=user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = client.get(self.url)
        a = ''