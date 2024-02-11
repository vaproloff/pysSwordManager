from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse

from .models import PasswordGenerationSettings
from .views import password_generator, pass_gen_api


class PasswordGeneratorViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_password_generator_authenticated_post(self):
        settings = PasswordGenerationSettings.objects.create(user=self.user)
        request = self.factory.post(reverse('generator'), data={})
        request.user = self.user
        response = password_generator(request)
        self.assertEqual(response.status_code, 200)

    def test_password_generator_authenticated_get(self):
        request = self.factory.get(reverse('generator'))
        request.user = self.user
        response = password_generator(request)
        self.assertEqual(response.status_code, 200)

    def test_password_generator_unauthenticated_post(self):
        request = self.factory.post(reverse('generator'), data={})
        request.user = AnonymousUser()
        response = password_generator(request)
        self.assertEqual(response.status_code, 200)

    def test_pass_gen_api_authenticated(self):
        settings = PasswordGenerationSettings.objects.create(user=self.user)
        request = self.factory.get(reverse('pass_gen_api'))
        request.user = self.user
        response = pass_gen_api(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

    def test_pass_gen_api_unauthenticated(self):
        request = self.factory.get(reverse('pass_gen_api'))
        request.user = AnonymousUser()
        response = pass_gen_api(request)
        self.assertEqual(response.status_code, 302)
