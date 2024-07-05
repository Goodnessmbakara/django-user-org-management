from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organisation

User = get_user_model()

class OrganisationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            firstName="John",
            lastName="Doe",
            email="john.doe@example.com",
            password="password123",
            phone="1234567890"
        )
        self.organisation = Organisation.objects.create(
            name="John's Organisation",
            description="Default organisation for John"
        )
        self.user.organisations.add(self.organisation)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))

    def test_get_user_details(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], "john.doe@example.com")

    def test_get_organisations(self):
        url = reverse('organisation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['organisations']), 1)

    def test_create_organisation(self):
        url = reverse('create-organisation')
        data = {
            "name": "New Organisation",
            "description": "New organisation description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "New Organisation")
