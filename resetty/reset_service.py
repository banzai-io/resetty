from datetime import date
from . import app_settings


def calculate_days_passed(last_password_update_at, target=date.today()):
    return (target - last_password_update_at).days


def password_has_due_date(password_details):
    last_password_update_at = password_details.password_last_updated_at
    # change to app_settings.RESET_PASSWORD_DELTA_DAYS
    return (
        calculate_days_passed(last_password_update_at)
        > app_settings.RESET_PASSWORD_DELTA
    )


def password_due(user):
    return not hasattr(user, "password_details") or password_has_due_date(
        user.password_details
    )


def path_excluded_from_redirect(current_path):
    # add these paths to the app_settings
    excluded_paths = [
        "/admin/login/",
        "/admin/logout/",
        "/admin/password_change/",
        "/admin/password_change/done/",
    ]

    return current_path.startswith("/accounts/reset/") or any(
        [current_path == path for path in excluded_paths]
    )


def should_reset_password(user):
    return (
        user.is_authenticated
        and any(
            [
                getattr(user, category)
                for category in app_settings.USER_CATEGORIES_REQUIRING_RESET
            ]
        )
        and password_due(user)
    )
