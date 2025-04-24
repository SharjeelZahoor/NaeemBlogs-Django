from django.core.cache import cache

def get_online_user_count():
    return len([key for key in cache._cache if key.startswith('online-')])
