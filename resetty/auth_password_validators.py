from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .app_settings import AUTH_VALIDATION_NO_REPEATED_PASSWORD_MESSAGE

# https://sixfeetup.com/blog/custom-password-validators-in-django


class DoNotReusePasswordValidator(object):
    def validate(self, password, user):
        if not user:
            return

        if authenticate(None, username=user.username, password=password):
            raise ValidationError(
                AUTH_VALIDATION_NO_REPEATED_PASSWORD_MESSAGE,
                code="password_not_changed",
            )

    def get_help_text(self):
        return "Please do not use your previous password"
