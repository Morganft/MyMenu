from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import new_receipt
from ..models import Receipt
from ..forms import NewReceiptForm


class NewReceiptTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        self.client.login(username='user1', password='123456')

    def test_success_status_code(self):
        url = reverse('new_receipt')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_view_url_resolves(self):
        view = resolve('/receipts/new_receipt/')
        self.assertEquals(view.func, new_receipt)

    def test_view_contains_link_back_to_receipts(self):
        url = reverse('new_receipt')
        url_receipts = reverse('receipts')
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(url_receipts))

    def test_view_contains_link_back_to_home(self):
        url = reverse('new_receipt')
        url_receipts = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'href="{0}"'.format(url_receipts))

    def test_csrf(self):
        url = reverse('new_receipt')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_valid_post_data(self):
        url = reverse('new_receipt')
        data = {
            'name': 'Just name',
            'amount': 1,
            'description': 'Just description'
        }
        self.client.post(url, data)
        self.assertTrue(Receipt.objects.exists())

    def test_invalid_post_data(self):
        url = reverse('new_receipt')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_invalid_post_data_empty_field(self):
        url = reverse('new_receipt')
        data = {
            'name': '',
            'amount': 0,
            'description': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Receipt.objects.exists())

    def test_contains_foem(self):
        url = reverse('new_receipt')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewReceiptForm)


class LoginRequiredNewReceiptTest(TestCase):
    def setUp(self):
        self.url = reverse('new_receipt')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
