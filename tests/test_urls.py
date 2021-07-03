from apps.logchecker import views
from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def test_url_home(self):
        url = reverse('logchecker:home')
        assert resolve(url).func == views.home
        assert resolve(url).view_name == "logchecker:home"


