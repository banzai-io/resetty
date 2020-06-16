from datetime import date
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import ResetPasswordExtra

User = get_user_model()


@receiver(post_save, sender=User)
def create_password_details(sender, instance, created, **kwargs):
    if created:
        password_details = ResetPasswordExtra(
            user=instance, password_last_updated_at=date.today()
        )
        password_details.save()


@receiver(pre_save, sender=User)
def set_last_password_update(sender, **kwargs):
    user = kwargs.get("instance")

    if user:
        new_password = user.password
        old_password = find_password_from_db(user)

        if new_password != old_password:
            create_or_update_password_last_update(user, date.today())


def create_or_update_password_last_update(user, the_date):
    if hasattr(user, "password_details"):
        password_details = user.password_details
        password_details.password_last_updated_at = the_date
    else:
        password_details = ResetPasswordExtra(
            user=user, password_last_updated_at=the_date
        )
    password_details.save()


def find_password_from_db(user):
    if User.objects.filter(pk=user.pk).exists():
        return User.objects.get(pk=user.pk).password
    return None
