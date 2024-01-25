from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware

from pysSword.settings import SHORT_SESSION_COOKIE_AGE


class ShortTermSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)

        last_activity = request.session.get('last_activity', None)
        if last_activity and timezone.now().timestamp() - last_activity > SHORT_SESSION_COOKIE_AGE:
            request.session['reauthenticate'] = True
        request.session['last_activity'] = timezone.now().timestamp()

