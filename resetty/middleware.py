from datetime import date
from django.http import HttpResponseRedirect

from .http import reset_password_redirect_url
from .models import ResetPasswordExtra
from .reset_service import (
    # password_due,
    path_excluded_from_redirect,
    should_reset_password,
)


class ResetPasswordMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            should_reset_password(request.user)
            and not path_excluded_from_redirect(request.path)
        ):
            # handle ?next url so a user goes back after resetting
            return HttpResponseRedirect(
                reset_password_redirect_url(request.user, request.path)
            )

        # the code above happens before subsequent middlewares in the stack and response

        response = self.get_response(request)

        # the code below will happen after response and previous middlewares in the stack

        return response
