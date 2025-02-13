from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from common.exception import LoginErrorMessages, UserValidationMessages

from ..models import User


class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="test@example.com",
            password=make_password("Qwe!@#123"),
            name="Test User"
        )
    def setUp(self):
        self.url = reverse('users:login')
    
    def test_sign_in_view(self):
        test_data = {
            'email': 'test@example.com',
            'password': 'Qwe!@#123',
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())
        
    def test_sign_in_with_wrong_email(self):
        test_data = {
            'email': 'wrong_email@example.com',
            'password': 'Qwe!@#123',
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], LoginErrorMessages.WRONG_EMAIL_OR_PASSWORD)
    
    def test_sign_in_with_wrong_password(self):
        test_data = {
            'email': 'test@example.com',
            'password': 'wrong_password',
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], LoginErrorMessages.WRONG_EMAIL_OR_PASSWORD)
        
    def test_sign_in_without_fields(self):
        test_data = {
            'password': 'Qwe!@#123',
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], UserValidationMessages.EMAIL_REQUIRED)
        
        test_data = {
            'email': 'test@example.com',
        }
        response = self.client.post(self.url, data=test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], UserValidationMessages.PASSWORD_REQUIRED)
        

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

class TokenCheckTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="test@example.com",
            password=make_password("Qwe!@#123"),
            name="Test User"
        )
        
    def setUp(self):
        self.url = reverse('users:check-token')
        
    def test_token_check_valid(self):
        # login
        login_response = self.client.post(
            reverse('users:login'),
            data={'email': 'test@example.com', 'password': 'Qwe!@#123'},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.json()['token']
        
        # # check token
        response = self.client.get(self.url, headers={'Content-Type': 'json', 'Authorization':  f'Token {token}'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.json())
        
    def test_token_check_invalid(self):
        response = self.client.get(self.url, headers={'Content-Type': 'json'}, format='json') # Not in token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], '잘못된 접근입니다.')
        

class LogoutTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            email="test@example.com",
            password=make_password("Qwe!@#123"),
            name="Test User"
        )
        
    def setUp(self):
        self.url = reverse('users:logout')
        
    def test_logout(self):
        # login
        login_response = self.client.post(
            reverse('users:login'),
            data={'email': 'test@example.com', 'password': 'Qwe!@#123'},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.json()['token']
        
        # logout
        response = self.client.post(self.url, headers={'Content-Type': 'json', 'Authorization':  f'Token {token}'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], True)
    
    def test_logout_invalid(self):
        response = self.client.post(self.url, headers={'Content-Type': 'json'}, format='json') # Not in token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], '잘못된 접근입니다.')