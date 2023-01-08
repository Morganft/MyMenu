from django.test import TestCase
from django.urls import reverse, resolve

from ..views import home


class HomeTests(TestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_placeholder(self):
        self.assertContains(
            self.response, 'Here is a placeholder for future home page')
