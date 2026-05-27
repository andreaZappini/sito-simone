# sitoArte/middleware.py
from django.contrib.auth import logout

class LogoutAdminOutsideAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        allowed_prefixes = [
            '/admin/',
            '/static/',
            '/media/',
        ]

        if request.user.is_authenticated and request.user.is_staff:
            if not any(path.startswith(prefix) for prefix in allowed_prefixes):
                logout(request)

        response = self.get_response(request)

        if path.startswith('/admin/'):
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return self.get_response(request)