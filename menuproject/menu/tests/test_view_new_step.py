from django.test import TestCase, override_settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .image_helper import ImageFactory, MOCK_MEDIA_ROOT

from ..models import Receipt, Step
from ..views import new_step
from ..forms import NewStepForm


class NewStepTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.receipt = Receipt.objects.create(name='Soup', amount=1, description='Just soup', created_by=user)
        self.url = reverse('new_step', kwargs={'receipt_pk': self.receipt.pk})


class LoginRequiredNewStepTests(NewStepTestCase):
    def test_redirections(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class NewStepTests(NewStepTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/receipts/{self.receipt.pk}/new_step/')
        self.assertEquals(view.func, new_step)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewStepForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, '<textarea', 1)
        self.assertContains(self.response, 'type="file"', 1)


@override_settings(MEDIA_ROOT=MOCK_MEDIA_ROOT)
class SuccessfulNewStepTests(NewStepTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.imageFactory = ImageFactory()
        image_file = self.imageFactory.getImage()
        test_image = SimpleUploadedFile('new_image.jpg', image_file.read())
        self.response = self.client.post(
            self.url, {'name': 'step 1', 'description': 'just make step 1', 'image': test_image})

    def test_redirections(self):
        receipt_url = reverse('receipt', kwargs={'pk': self.receipt.pk})
        self.assertRedirects(self.response, receipt_url)

    def test_step_created(self):
        self.assertEquals(Step.objects.count(), 1)

    def tearDown(self) -> None:
        self.imageFactory.cleanUp()
        return super().tearDown()


class InvalidNewStepTests(NewStepTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
