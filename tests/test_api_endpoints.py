from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.logchecker.models import District, Log
from django.contrib.auth.models import User


class TestsDistrict(APITestCase):

    def test_district_views(self):
        url = reverse('restapi:client-list')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        
