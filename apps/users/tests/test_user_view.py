from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from common.exception import UserValidationMessages

from ..models import User


class SignUpTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="duplicated@example.com",
            password=make_password("Qwe!@#123"),
            name="Duplicated User"
        )
    
    def setUp(self):
        self.url = reverse('users:sign-up')
    def test_sign_up_view(self):
        test_data = {
            'email': 'test@example.com',
            'password': 'Qwe!@#123',
            'name': 'Test User'
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['created'], True)
    
    def test_sign_up_duplicate_email(self):
        test_data = {
            'email': 'duplicated@example.com',
            'password': 'Qwe!@#123',
            'name': 'Duplicated User'
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()['message'], UserValidationMessages.EMAIL_ALREADY_EXISTS)
        
    def test_sign_up_without_email(self):
        test_data = {
            'password': 'Qwe!@#123',
            'name': 'Test User'
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], UserValidationMessages.EMAIL_REQUIRED)
        
    def test_sign_up_without_password(self):
        test_data = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], UserValidationMessages.PASSWORD_REQUIRED)
        
    def test_sign_up_without_name(self):
        test_data = {
            'email': 'test@example.com',
            'password': 'Qwe!@#123'
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], UserValidationMessages.NAME_REQUIRED)