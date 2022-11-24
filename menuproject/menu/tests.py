from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, receipt, new_ingredient
from django.contrib.auth.models import User
from .models import Receipt

# Create your tests here.
class HomeTests(TestCase):
  def setUp(self):
    self.user = User.objects.create(username='user1', email='user1@mail.com', password='123456')
    self.receipt = Receipt.objects.create(name='Soup', description='Simple Soup', created_by=self.user)
    url = reverse('home')
    self.response = self.client.get(url)

  def test_home_view_status_code(self):
    self.assertEquals(self.response.status_code, 200)

  def test_home_url_resolves_home_view(self):
    view = resolve('/')
    self.assertEquals(view.func, home)

  def test_home_view_contains_link_to_receipt_page(self):
    receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
    self.assertContains(self.response, 'href="{0}"'.format(receipt_url))

class ReceiptTests(TestCase):
  def setUp(self):
    self.user = User.objects.create(username='user1', email='user1@mail.com', password='123456')
    self.receipt = Receipt.objects.create(name='Soup', description='Simple Soup', created_by=self.user)
  
  def test_receipt_view_success_status_code(self):
    url = reverse('receipt', kwargs={'pk': self.receipt.pk})
    response = self.client.get(url)
    self.assertEquals(response.status_code, 200)

  def test_receipt_view_not_found_status_code(self):
    url = reverse('receipt', kwargs={'pk': 99})
    response = self.client.get(url)
    self.assertEquals(response.status_code, 404)

  def test_receipt_url_resolves_receipt_view(self):
    view = resolve(f'/receipts/{self.receipt.pk}/')
    self.assertEquals(view.func, receipt)

  def test_receipt_view_contains_link_back_to_homepage(self):
    receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
    response = self.client.get(receipt_url)
    homepage_url = reverse('home')
    self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewIngredient(TestCase):
  def setUp(self):
    self.user = User.objects.create(username='user1', email='user1@mail.com', password='123456')
    self.receipt = Receipt.objects.create(name='Soup', description='Simple Soup', created_by=self.user)

  def test_new_ingredient_view_success_status_code(self):
    url = reverse('new_ingredient', kwargs={'receipt_pk': self.receipt.pk})
    response = self.client.get(url)
    self.assertEquals(response.status_code, 200)

  def test_new_ingredient_view_not_found_status_code(self):
    url = reverse('new_ingredient', kwargs={'receipt_pk': 99})
    response = self.client.get(url)
    self.assertEquals(response.status_code, 404)

  def test_new_ingredient_url_resolves_new_ingredient_view(self):
    view = resolve('/receipts/1/new_ingredient/')
    self.assertEquals(view.func, new_ingredient)

  def test_new_ingredient_view_contains_link_back_to_receipt(self):
    new_ingredient_url = reverse('new_ingredient', kwargs={'receipt_pk': self.receipt.pk})
    receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
    response = self.client.get(new_ingredient_url)
    self.assertContains(response, 'href="{0}"'.format(receipt_url))
