import datetime
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache

class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # create session if it doesn't exist
            session_key = request.session.session_key
        
        # Save current time in cache with a 5-minute expiry
        cache.set(f'online-{session_key}', datetime.datetime.now(), timeout=300)
