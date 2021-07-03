import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from apps.logchecker import views


class TestViews(TestCase):

    def setUp(self):
        # mixer.blend('logchecker.User')
        self.client = Client()
        self.home_url = reverse('logchecker:home')
        self.user1 = mixer.blend(User)

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)
        assert response.status_code == 302
        assert 'accounts/login' in response.url

    def test_home_view_POST(self):
        request = RequestFactory().post(self.home_url)
        request.user = self.user1
        response = views.home(request)
        assert response.status_code == 302

    def test_homeview_get(self):
        request = RequestFactory().get('/home/')
        request.user = self.user1
        response = views.HomeView.as_view()(request)    
        assert response.status_code == 302


# @pytest.mark.django_db
def test_home_view_GET_mix(db):
    request = RequestFactory().get('logchecker:home')
    request.user = mixer.blend(User)
    response = views.home(request)
    assert response.status_code == 200
