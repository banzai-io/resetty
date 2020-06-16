from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

# https://sixfeetup.com/blog/custom-password-validators-in-django

class DoNotReusePasswordValidator(object):
    def validate(self, password, user):
        if not user:
            return

        if authenticate(None, username=user.username, password=password):
            raise ValidationError(
                "Do not use your old password", code="password_not_changed",
            )

    def get_help_text(self):
        return "Please do not use your previous password"
