from allauth.account.reauthentication import record_authentication
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from pass_keeper.models import PasswordEntry
from pass_keeper.views import create_password, password_list, delete_password, edit_password


class PasswordKeeperTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_password_list_view(self):
        password_entry = PasswordEntry.objects.create(user=self.user, title='Test Password 1', website='example.com',
                                                      username='testuser', encrypted_password=b'encrypted_password1')

        request = self.factory.get(reverse('create_password'))
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        response = password_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, password_entry.title)

    def test_create_password_view(self):
        post_data = {'title': 'New Password', 'website': 'example.com', 'username': 'testuser',
                     'password': 'testpassword'}
        request = self.factory.post(reverse('create_password'), data=post_data)
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = create_password(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PasswordEntry.objects.filter(user=self.user, title='New Password').exists())

    def test_edit_password_view(self):
        password = PasswordEntry.objects.create(user=self.user, title='Test Password', website='example.com',
                                                username='testuser', encrypted_password=b'encrypted_password')
        post_data = {'title': 'Updated Password', 'website': 'example.org',
                     'username': 'testuser', 'password': 'testpassword'}

        request = self.factory.post(reverse('edit_password', kwargs={'entry_id': password.id}), data=post_data)
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = edit_password(request, entry_id=password.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PasswordEntry.objects.filter(user=self.user, title='Updated Password').exists())

    def test_delete_password_view(self):
        password = PasswordEntry.objects.create(user=self.user, title='Test Password', website='example.com',
                                                username='testuser', encrypted_password=b'encrypted_password')

        request = self.factory.get(reverse('delete_password', kwargs={'entry_id': password.id}))
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = delete_password(request, entry_id=password.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PasswordEntry.objects.filter(user=self.user, title='Test Password').exists())
