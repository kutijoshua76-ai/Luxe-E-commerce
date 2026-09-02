from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse, resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path
            
            # Define allowed paths
            exempt_urls = [
                reverse('login'),
                reverse('register'),
                '/account/logout/',
            ]
            
            # Check if path is exempt or starts with admin/static/media
            is_exempt = any(path == url or path == url.rstrip('/') for url in exempt_urls)
            is_admin = path.startswith('/admin/')
            is_static = path.startswith(settings.STATIC_URL)
            is_media = path.startswith(settings.MEDIA_URL)
            
            if not (is_exempt or is_admin or is_static or is_media):
                # Ensure we redirect to the absolute LOGIN_URL
                login_url = settings.LOGIN_URL
                if not login_url.startswith('/'):
                    login_url = reverse(login_url)
                return redirect(f"{login_url}?next={path}")

        return self.get_response(request)
