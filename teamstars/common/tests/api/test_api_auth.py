from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

TEST_USER = 'scortest'
TEST_PASSWORD = 'justatestpassword'


class AuthTestCase(APITestCase):
    def test_get_token_empty_payload(self):
        response = self.client.post('/api/v1/token-auth/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", str(response.data))

    def test_get_token_bad_username_password(self):
        response = self.client.post('/api/v1/token-auth/', {
            'username': 'bad',
            'password': 'credentials',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Unable to log in with provided credentials.", str(response.data))

    def test_get_token_happy_path(self):
        User.objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        response = self.client.post('/api/v1/token-auth/', {
            'username': TEST_USER,
            'password': TEST_PASSWORD,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", str(response.data))
