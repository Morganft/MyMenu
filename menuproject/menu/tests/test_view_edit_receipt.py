from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm

from ..models import Receipt
from ..views import ReceiptUpdateView


class ReceiptUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.receipt = Receipt.objects.create(name='Soup', amount=1, description='Just soup', created_by=user)
        self.url = reverse('edit_receipt', kwargs={
            'pk': self.receipt.pk,
        })


class LoginRequiredReceiptUpdateViewTests(ReceiptUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedReceiptUpdateView(ReceiptUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class ReceiptUpdateViewTests(ReceiptUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(f'/receipts/{self.receipt.pk}/edit/')
        self.assertEquals(view.func.view_class, ReceiptUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReceiptUpdateViewTests(ReceiptUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {'name': self.receipt.name, 'amount': 2, 'description': 'new description'})

    def test_redirection(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertRedirects(self.response, receipt_url)

    def test_receipt_changed(self):
        self.receipt.refresh_from_db()
        self.assertEquals(self.receipt.description, 'new description')
        self.assertEquals(self.receipt.amount, 2)


class InvalidReceiptUpdateViewTests(ReceiptUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
