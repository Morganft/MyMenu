from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ..models import Receipt, Ingredient, IngredientType
from ..views import IngredientDeleteView


class DeleteIngredientTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.receipt = Receipt.objects.create(name='Soup', description='Just soup', created_by=user)
        ingredient_type = IngredientType.objects.create(name="Just name")
        self.ingredient = Ingredient.objects.create(type=ingredient_type, amount=4, receipt=self.receipt)
        self.url = reverse('delete_ingredient', kwargs={'receipt_pk': self.receipt.pk, 'pk': self.ingredient.pk})


class LoginRequiredDeleteIngredientTests(DeleteIngredientTestCase):
    def test_redirections(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedIngredientDeleteViewTests(DeleteIngredientTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)
        self.post_response = self.client.get(self.url)

    def test_get_status_code(self):
        self.assertEquals(self.response.status_code, 404)

    def test_post_status_code(self):
        self.assertEquals(self.post_response.status_code, 404)


class DeleteIngredientTests(DeleteIngredientTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(f'/receipts/{self.receipt.pk}/ingredients/{self.ingredient.pk}/delete/')
        self.assertEquals(view.func.view_class, IngredientDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_view_contains_link_back_to_receipt(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertContains(self.response, receipt_url)

    def test_form_input(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<button', 1)


class SuccessfullIngredientDeleteViewTests(DeleteIngredientTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url)

    def test_redirection(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertRedirects(self.response, receipt_url)

    def test_step_deleted(self):
        self.assertEquals(Ingredient.objects.count(), 0)
