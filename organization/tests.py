from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organisation

User = get_user_model()

class OrganisationTests(APITestCase):
    def setUp(self):        
        self.user1 = User.objects.create_user(
            firstName="John",
            lastName="Doe",
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
            firstName="Jane",
            lastName="Doe",
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

    def test_get_organisations(self):
        url = reverse('organisation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['organisations']), 2)

    def test_create_organisation(self):
        url = reverse('create-organisation')
        data = {
            "name": "New Organisation",
            "description": "New organisation description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "New Organisation")
    
    def test_user_cannot_access_other_organisation(self):
        # Authenticate as user1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.refresh1.access_token))
        response = self.client.get(reverse('organisation-detail', args=[self.organisation2.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access_own_organisation(self):
        # Authenticate as user1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.refresh1.access_token))
        response = self.client.get(reverse('organisation-detail', args=[self.organisation1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], "John's Organisation")
