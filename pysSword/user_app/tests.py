from allauth.account.reauthentication import record_authentication
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage

from user_app.views import user_profile


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.factory = RequestFactory()

    def test_user_profile_get(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        response = user_profile(request)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_post_change_first_name(self):
        request = self.factory.post(reverse('profile'), data={'form_type': 'first_name', 'first_name': 'NewFirstName'})
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = user_profile(request)
        self.assertEqual(self.user.first_name, 'NewFirstName')

    def test_user_profile_post_change_last_name(self):
        request = self.factory.post(reverse('profile'), data={'form_type': 'last_name', 'last_name': 'NewLastName'})
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = user_profile(request)
        self.assertEqual(self.user.last_name, 'NewLastName')

    def test_user_profile_post_change_password(self):
        request = self.factory.post(reverse('profile'), data={'form_type': 'password', 'oldpassword': 'testpassword',
                                                              'password1': 'newtestpassword',
                                                              'password2': 'newtestpassword'})
        request.user = self.user
        SessionMiddleware(lambda x: x).process_request(request)
        record_authentication(request, self.user)
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = user_profile(request)
        self.assertTrue(self.user.check_password('newtestpassword'))
