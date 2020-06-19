from django.conf import settings

settings.configure(
    {
        "RESETTY_USER_CATEGORIES_REQUIRING_RESET": ["is_staff"],
        "RESETTY_RESET_PASSWORD_DELTA_DAYS": 30,
    },
)

import arrow
import pytest
from pytest_mock import mocker
from collections import namedtuple

from resetty.resetty.reset_service import (
    calculate_days_passed,
    password_due,
    path_excluded_from_redirect,
    should_reset_password,
)
from resetty.resetty import app_settings

User = namedtuple(
    "User", ["name", "is_authenticated", "is_staff", "is_superuser", "password_details"]
)
User.__new__.__defaults__ = ("Ignacio", False, False, False, None)
Password = namedtuple("ResetPasswordExtra", ["password_last_updated_at"])


@pytest.fixture
def user_with_no_password_details():
    # user does not have the 'password_details' attribute
    UserWithNoPswdDetails = namedtuple("User", ["name", "is_authenticated"])
    return UserWithNoPswdDetails(name="Ignacio", is_authenticated=True)


@pytest.fixture
def user_with_password_updated_recently():
    ten_days_ago = arrow.utcnow().shift(days=-10).date()
    return User(
        name="Ignacio", password_details=Password(password_last_updated_at=ten_days_ago)
    )


@pytest.fixture
def user_with_password_updated_long_time_ago():
    thirty_days_ago = (
        arrow.utcnow().shift(days=-(app_settings.RESET_PASSWORD_DELTA_DAYS + 1)).date()
    )
    return User(
        name="Ignacio",
        is_authenticated=True,
        password_details=Password(password_last_updated_at=thirty_days_ago),
    )


@pytest.fixture
def staff_user(user_with_password_updated_long_time_ago):
    temp = user_with_password_updated_long_time_ago._asdict()
    temp["is_staff"] = True
    return User(**temp)


@pytest.fixture
def super_user(user_with_password_updated_long_time_ago):
    temp = user_with_password_updated_long_time_ago._asdict()
    temp["is_superuser"] = True
    return User(**temp)


def test_calculate_days_passed():
    now = arrow.utcnow()
    # test 31 days before
    days_before_as_arrow = now.floor("day").shift(days=-31)
    days_before_as_date = days_before_as_arrow.datetime.date()
    assert calculate_days_passed(days_before_as_date) == 31


def test_password_last_update_has_not_been_set(user_with_no_password_details):
    assert password_due(user_with_no_password_details) is True


def test_password_last_update_is_none():
    user = User(name="Ignacio", is_authenticated=True, password_details=None)
    assert password_due(user) is True


def test_user_with_last_update_within_threshold(user_with_password_updated_recently):
    assert password_due(user_with_password_updated_recently) is False


def test_user_with_last_update_outside_threshold(
    user_with_password_updated_long_time_ago,
):
    assert password_due(user_with_password_updated_long_time_ago) is True


def test_user_needing_reset_not_authenticated(
    mocker, user_with_password_updated_long_time_ago
):
    temp = user_with_password_updated_long_time_ago._asdict()
    temp["is_authenticated"] = False
    non_auth_user = User(**temp)
    assert should_reset_password(non_auth_user) is False


def test_staff_user_requires_reset_by_default(staff_user):
    assert should_reset_password(staff_user) is True


def test_staff_user_requires_reset_by_default(monkeypatch, staff_user):
    monkeypatch.setattr(app_settings, "USER_CATEGORIES_REQUIRING_RESET", [])
    assert should_reset_password(staff_user) is False


def test_super_user_skips_reset_by_default(super_user):
    assert should_reset_password(super_user) is False


def test_super_user_requires_reset_by_settings(monkeypatch, super_user):
    monkeypatch.setattr(
        app_settings, "USER_CATEGORIES_REQUIRING_RESET", ["is_superuser"]
    )
    assert should_reset_password(super_user) is True


def test_default_paths_excluded_from_redirect():
    default_excluded_paths = [
        "/accounts/reset/",
        "/accounts/reset/123/gq/"
        "/admin/login/",
        "/admin/logout/",
        "/admin/password_change/",
        "/admin/password_change/done/",
        "/reset/",
        "/reset/123/gq/"
    ]

    for path in default_excluded_paths:
        assert path_excluded_from_redirect(path)


def test_default_and_configured_paths_excluded_from_redirect(monkeypatch):
    custom_paths = ["/mypersonal/path"]
    monkeypatch.setattr(app_settings, "REDIRECT_EXCLUDED_PATHS", custom_paths)

    default_excluded_paths = [
        "/accounts/reset/",
        "/admin/login/",
        "/admin/logout/",
        "/admin/password_change/",
        "/admin/password_change/done/",
    ]

    for path in default_excluded_paths + custom_paths:
        assert path_excluded_from_redirect(path)
