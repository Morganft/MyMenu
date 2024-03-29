from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import ReceiptsListView
from ..models import Receipt


class ReceiptsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        self.receipt = Receipt.objects.create(
            name='Soup', amount=1, description='Simple Soup', created_by=self.user)
        url = reverse('receipts')
        self.response = self.client.get(url)

    def test_receipts_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_receipts_url_resolves_receipts_view(self):
        view = resolve('/receipts/')
        self.assertEquals(view.func.view_class, ReceiptsListView)

    def test_receipts_view_contains_link_to_receipt_page(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertContains(self.response, 'href="{0}"'.format(receipt_url))


class ReceiptsTestsWithTags(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@mail.com', password='123456')
        self.receipt = Receipt.objects.create(
            name='Soup', amount=1, description='Simple Soup', created_by=self.user)
        self.tag = self.receipt.tags.create(name="tag1")

        url = reverse('receipts_tag', kwargs={
            'tag_id': self.tag.pk,
        })
        self.response = self.client.get(url)

    def test_receipts_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_receipts_url_resolves_receipts_view(self):
        view = resolve(f'/receipts/tag/{self.tag.pk}')
        self.assertEquals(view.func.view_class, ReceiptsListView)

    def test_receipts_view_contains_link_to_receipt_page(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertContains(self.response, 'href="{0}"'.format(receipt_url))
        self.assertContains(self.response, f': {self.tag.name}')
