import re
from datetime import datetime, timezone
from . import app_settings


def today():
    return datetime.now(timezone.utc).date()


def calculate_days_passed(last_password_update_at, target=today()):
    return (target - last_password_update_at).days


def password_has_due_date(password_details):
    last_password_update_at = password_details.password_last_updated_at
    return (
        calculate_days_passed(last_password_update_at)
        >= app_settings.RESET_PASSWORD_DELTA_DAYS
    )


def password_due(user):
    return not (
        hasattr(user, "password_details") and user.password_details
    ) or password_has_due_date(user.password_details)


def path_excluded_from_redirect(current_path):
    # add these paths to the app_settings
    excluded_paths = app_settings.REDIRECT_EXCLUDED_PATHS + [
        "/admin/login/",
        "/admin/logout/",
        "/admin/password_change/",
        "/admin/password_change/done/",
    ]

    pattern = r"\/?(.+)?\/reset\/?"

    return re.match(pattern, current_path) or any(
        [current_path == path for path in excluded_paths]
    )


def user_within_categories_requiring_reset(user):
    return any(
        [
            getattr(user, category)
            for category in app_settings.USER_CATEGORIES_REQUIRING_RESET
        ]
    )


def should_reset_password(user):
    return (
        user.is_authenticated
        and user_within_categories_requiring_reset(user)
        and password_due(user)
    )
