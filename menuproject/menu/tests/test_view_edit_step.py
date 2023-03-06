from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from django.forms import ModelForm
from django.core.files.uploadedfile import SimpleUploadedFile

from .image_helper import ImageFactory, MOCK_MEDIA_ROOT

from ..models import Receipt, Step
from ..views import StepUpdateView


class StepUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.receipt = Receipt.objects.create(name='Soup', description='Just soup', created_by=user)
        self.step = Step.objects.create(name='Main step', description='Make a soup', receipt=self.receipt)
        self.url = reverse('edit_step', kwargs={
            'receipt_pk': self.receipt.pk,
            'step_pk': self.step.pk
        })


class LoginRequiredStepUpdateViewTests(StepUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{login_url}?next={self.url}')


class UnauthorizedStepUpdateCiew(StepUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class StepUpdateViewTests(StepUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve(f'/receipts/{self.receipt.pk}/steps/{self.step.pk}/edit/')
        self.assertEquals(view.func.view_class, StepUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_input(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, 'type="file"', 1)


@override_settings(MEDIA_ROOT=MOCK_MEDIA_ROOT)
class SuccessfulStepUpdateViewTests(StepUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.imageFactory = ImageFactory()
        image_file = self.imageFactory.getImage()
        test_image = SimpleUploadedFile('new_image.jpg', image_file.read())
        self.response = self.client.post(
            self.url, {'name': self.step.name, 'description': 'new description', 'image': test_image})

    def test_redirection(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertRedirects(self.response, receipt_url)

    def test_step_changed(self):
        self.step.refresh_from_db()
        self.assertEquals(self.step.description, 'new description')

    def tearDown(self) -> None:
        self.imageFactory.cleanUp()
        return super().tearDown()


class InvalidStepUpdateViewTests(StepUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
