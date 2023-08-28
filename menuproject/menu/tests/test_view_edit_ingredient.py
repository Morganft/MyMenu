from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm

from ..models import Receipt, Ingredient, IngredientType
from ..views import IngredientUpdateView


class IngredientUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.receipt = Receipt.objects.create(name='Soup', amount=1, description='Just soup', created_by=user)
        self.ingredient_type = IngredientType.objects.create(name='Tomato')
        self.new_ingredient_type = IngredientType.objects.create(name='Onion')
        self.ingredient = Ingredient.objects.create(amount=10, receipt=self.receipt, type=self.ingredient_type)
        self.url = reverse('edit_ingredient', kwargs={
            'receipt_pk': self.receipt.pk,
            'ingredient_pk': self.ingredient.pk
        })


class LoginRequiredIngredientUpdateViewTests(IngredientUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedIngredientUpdateView(IngredientUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class IngredientUpdateViewTests(IngredientUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(f'/receipts/{self.receipt.pk}/ingredients/{self.ingredient.pk}/edit/')
        self.assertEquals(view.func.view_class, IngredientUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, '<select', 1)


class SuccessfulIngredientUpdateViewTests(IngredientUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {'type': self.new_ingredient_type.pk, 'amount': 20})

    def test_redirection(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertRedirects(self.response, receipt_url)

    def test_ingredient_changed(self):
        self.ingredient.refresh_from_db()
        self.assertEquals(self.ingredient.amount, '20')
        self.assertEquals(self.ingredient.type, self.new_ingredient_type)


class InvalidIngredientUpdateViewTests(IngredientUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
