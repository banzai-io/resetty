from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# pull today from the service so it is consistent across this package
from .reset_service import today
from .models import ResetPasswordExtra

User = get_user_model()


@receiver(post_save, sender=User)
def create_password_details(sender, instance, created, **kwargs):
    """ Makes sure we save the password details only after the user instance is saved."""
    if created:
        instance.password_details = ResetPasswordExtra(
            user=instance, password_last_updated_at=today()
        )

    instance.password_details.save()


@receiver(pre_save, sender=User)
def set_last_password_update(sender, **kwargs):
    user = kwargs.get("instance")

    if user:
        new_password = user.password
        old_password = find_password_from_db(user)

        if new_password != old_password or not hasattr(user, "password_details"):
            # this makes sure that the update only happens on password change.
            create_or_update_password_last_update(user, today())


def create_or_update_password_last_update(user, the_date):
    # assigns a new password details object or updates an existing one.
    # BUT will only be saved after the user instance is saved.
    if hasattr(user, "password_details"):
        password_details = user.password_details
        password_details.password_last_updated_at = the_date
    else:
        password_details = ResetPasswordExtra(
            user=user, password_last_updated_at=the_date
        )


def find_password_from_db(user):
    if User.objects.filter(pk=user.pk).exists():
        return User.objects.get(pk=user.pk).password
    return None
