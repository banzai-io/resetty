from django.urls import reverse
from .app_settings import RESET_PASSWORD_URL


def reset_password_redirect_url(user, path):
    # default is /admin/password_change/
    redirect_to = RESET_PASSWORD_URL or reverse("admin:password_change")
    return f"{redirect_to}?next={path}"
