from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@email.com', password='testpassword')

    def test_index_view(self):
        self.client.login(email='testuser@email.com', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/index.html')
        self.assertEqual(response.context['title'], 'Главная')
        self.assertEqual(response.context['user'], self.user)
