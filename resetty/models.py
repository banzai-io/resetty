from django.conf import settings
from django.db import models
from django.db.models.fields import DateField


class ResetPasswordExtra(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        primary_key=True,
        related_name="password_details",
    )
    password_last_updated_at = DateField()
