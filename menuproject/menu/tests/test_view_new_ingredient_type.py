from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import new_ingredient_type
from ..models import IngredientType
from ..forms import NewIngredientTypeForm


class NewIngredeintTypeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        self.client.login(username='user1', password='123456')

    def test_success_status_code(self):
        url = reverse('new_ingredient_type')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_url_resolves(self):
        view = resolve('/ingredient_types/new_ingredient_type/')
        self.assertEquals(view.func, new_ingredient_type)

    def test_view_contains_link_back_to_receipts(self):
        url = reverse('new_ingredient_type')
        url_receipts = reverse('ingredient_types')
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(url_receipts))

    def test_view_contains_link_back_to_home(self):
        url = reverse('new_ingredient_type')
        url_receipts = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(url_receipts))

    def test_csrf(self):
        url = reverse('new_ingredient_type')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_valid_post_data(self):
        url = reverse('new_ingredient_type')
        data = {
            'name': 'Just name',
        }
        self.client.post(url, data)
        self.assertTrue(IngredientType.objects.exists())

    def test_invalid_post_data(self):
        url = reverse('new_ingredient_type')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_invalid_post_data_empty_field(self):
        url = reverse('new_ingredient_type')
        data = {
            'name': '',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(IngredientType.objects.exists())

    def test_contains_foem(self):
        url = reverse('new_ingredient_type')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewIngredientTypeForm)


class LoginRequiredNewIngredientTypeTest(TestCase):
    def setUp(self):
        self.url = reverse('new_ingredient_type')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
