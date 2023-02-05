from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import ModelForm

from ..models import IngredientType
from ..views import IngredientTypeUpdateView


class IngredientTypeUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.ingredient_type = IngredientType.objects.create(name='Test ingredient type')
        self.url = reverse('edit_ingredient_type', kwargs={
            'ingredient_type_pk': self.ingredient_type.pk
        })


class LoginRequiredIngredientUpdateViewTests(IngredientTypeUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedStepUpdateCiew(IngredientTypeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


class StepUpdateViewTests(IngredientTypeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(f'/ingredient_types/{self.ingredient_type.pk}/edit/')
        self.assertEquals(view.func.view_class, IngredientTypeUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        self.assertContains(self.response, '<input', 2)


class SuccessfulStepUpdateViewTests(IngredientTypeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'name': 'New name'})

    def test_redirection(self):
        ingredient_type_url = reverse('ingredient_types')
        self.assertRedirects(self.response, ingredient_type_url)

    def test_step_changed(self):
        self.ingredient_type.refresh_from_db()
        self.assertEquals(self.ingredient_type.name, 'New name')


class InvalidStepUpdateViewTests(IngredientTypeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
