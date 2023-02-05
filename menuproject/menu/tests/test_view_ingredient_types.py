from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import IngredientTypesListView


class IngredientTypesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        url = reverse('ingredient_types')
        self.response = self.client.get(url)

    def test_ingredient_types_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_ingredient_types_url_resolves_receipts_view(self):
        view = resolve('/ingredient_types/')
        self.assertEquals(view.func.view_class, IngredientTypesListView)
