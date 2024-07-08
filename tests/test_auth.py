from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from organization.models import Organisation

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def test_register_user_successfully_with_default_organisation(self):
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['user']['first_name'], "John")
        self.assertIn("Organisation", response.data['data']['user']['first_name'] + "'s Organisation")

    def test_user_login_successfully(self):
        User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        url = reverse('login')
        data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], "john.doe@example.com")

    def test_missing_required_fields(self):
        url = reverse('register')
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)

    def test_duplicate_email(self):
        User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        url = reverse('register')
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "0987654321"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)

class OrganisationAccessTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        self.organisation1 = Organisation.objects.create(
            name="John's Organisation",
            description="Default organisation for John"
        )
        self.user1.organisations.add(self.organisation1)

        self.user2 = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            password="password123",
            phone="0987654321"
        )
        self.organisation2 = Organisation.objects.create(
            name="Jane's Organisation",
            description="Default organisation for Jane"
        )
        self.user2.organisations.add(self.organisation2)

        self.refresh1 = RefreshToken.for_user(self.user1)
        self.refresh2 = RefreshToken.for_user(self.user2)

    def test_user_cannot_access_other_organisation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.refresh1.access_token))
        response = self.client.get(reverse('organisation-detail', args=[self.organisation2.org_id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access_own_organisation(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.refresh1.access_token))
        response = self.client.get(reverse('organisation-detail', args=[self.organisation1.org_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], "John's Organisation")

class TokenGenerationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(
            name="John's Organisation",
            description="Default organisation for John"
        )
        self.user.organisations.add(self.organisation)

    def test_token_generation(self):
        refresh = RefreshToken.for_user(self.user)
        self.assertIn('access', refresh.access_token['token_type'])
        self.assertIn('refresh', refresh['token_type'])
        self.assertEqual(refresh['user_id'], (self.user.id))

    def test_token_expiry(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token

        response = self.client.get(reverse('user-detail', args=[self.user.id]), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        from datetime import timedelta
        access_token.set_exp(lifetime=timedelta(seconds=0))
        response = self.client.get(reverse('user-detail', args=[self.user.user_id]), HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

