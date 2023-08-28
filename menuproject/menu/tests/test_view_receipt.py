from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import receipt
from ..models import Receipt


class ReceiptTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        self.receipt = Receipt.objects.create(
            name='Soup', amount=1, description='Simple Soup', created_by=self.user)

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
        homepage_url = reverse('home')
        new_ingredient_url = reverse('new_ingredient', kwargs={
                                     'receipt_pk': self.receipt.pk})

        response = self.client.get(receipt_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_ingredient_url))

    def test_receipt_view_contains_link_back_to_receipts(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        receipts_url = reverse('receipts')
        new_ingredient_url = reverse('new_ingredient', kwargs={
                                     'receipt_pk': self.receipt.pk})

        response = self.client.get(receipt_url)
        self.assertContains(response, 'href="{0}"'.format(receipts_url))
        self.assertContains(response, 'href="{0}"'.format(new_ingredient_url))
