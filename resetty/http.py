from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# how do we support another token_generator?
def account_reset_password_redirect_url(user, token_generator=default_token_generator):
    path_params = {
        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
    }
    return reverse("password_reset_confirm", kwargs=path_params)


def reset_password_redirect_url(user, path):
    redirect_to =  (
        reverse("admin:password_change")
        if path.startswith("/admin/")
        else account_reset_password_redirect_url(user)
    )
    return f"{redirect_to}?next={path}"
