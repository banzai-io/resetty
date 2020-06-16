from django.conf import settings

settings.configure(
    {"RESETTY_USER_CATEGORIES_REQUIRING_RESET": [],}
)

import arrow
import pytest
from resetty.resetty.reset_service import calculate_days_passed


def test_calculate_days_passed():
    now = arrow.utcnow()
    # test 31 days before
    days_before_as_arrow = now.floor("day").shift(days=-31)
    days_before_as_date = days_before_as_arrow.datetime.date()
    assert calculate_days_passed(days_before_as_date) == 30
