from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from common.tests.api.test_api_auth import TEST_USER, TEST_PASSWORD


class UsersTestCase(APITestCase):
    token = None

    def setUp(self):
        User.objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        token_response = self.client.post('/api/v1/token-auth/', {
            'username': TEST_USER,
            'password': TEST_PASSWORD,
        }, format='json')
        self.token = token_response.data.get('token')

    def test_endpoint_without_token(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_right_number_of_users(self):
        for i in range(30):
            User.objects.create_user(username=TEST_USER + str(i), password=TEST_PASSWORD)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additional one user because of the setUp step
        self.assertEqual(31, len(response.data))
