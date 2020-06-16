from django.conf import settings

settings.configure(
    {
        "RESETTY_USER_CATEGORIES_REQUIRING_RESET": [],
        "RESETTY_RESET_PASSWORD_DELTA_DAYS": 30,
    },
)

import arrow
import pytest
from collections import namedtuple

from resetty.resetty.reset_service import calculate_days_passed, password_due
from resetty.resetty.app_settings import RESET_PASSWORD_DELTA_DAYS

Password = namedtuple("ResetPasswordExtra", ["password_last_updated_at"])


@pytest.fixture
def user_with_no_password_details():
    # user does not have the 'password_details' attribute
    User = namedtuple("User", ["name"])
    return User(name="Ignacio")


@pytest.fixture
def user_with_password_updated_recently():
    User = namedtuple("User", ["name", "password_details"])
    ten_days_ago = arrow.utcnow().shift(days=-10).date()
    return User(
        name="Ignacio", password_details=Password(password_last_updated_at=ten_days_ago)
    )


@pytest.fixture
def user_with_password_updated_long_time_ago():
    User = namedtuple("User", ["name", "password_details"])
    thirty_days_ago = (
        arrow.utcnow().shift(days=-(RESET_PASSWORD_DELTA_DAYS+1)).date()
    )
    return User(
        name="Ignacio",
        password_details=Password(password_last_updated_at=thirty_days_ago),
    )


def test_calculate_days_passed():
    now = arrow.utcnow()
    # test 31 days before
    days_before_as_arrow = now.floor("day").shift(days=-31)
    days_before_as_date = days_before_as_arrow.datetime.date()
    assert calculate_days_passed(days_before_as_date) == 30


def test_password_last_update_has_not_been_set(user_with_no_password_details):
    assert password_due(user_with_no_password_details) is True


def test_user_with_last_update_within_threshold(user_with_password_updated_recently):
    assert password_due(user_with_password_updated_recently) is False


def test_user_with_last_update_outside_threshold(user_with_password_updated_long_time_ago):
    assert password_due(user_with_password_updated_long_time_ago) is True
