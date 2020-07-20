from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# pull today from the service so it is consistent across this package
from .reset_service import today, user_within_categories_requiring_reset
from .models import ResetPasswordExtra

User = get_user_model()


def user_should_set_password_details_skipping_reset(user):
    return not hasattr(
        user, "password_details"
    ) and not user_within_categories_requiring_reset(user)


def has_attr_present(obj, attr_name):
    return hasattr(obj, attr_name) and getattr(obj, attr_name)


@receiver(post_save, sender=User)
def create_password_details(sender, instance, created, **kwargs):
    """ Makes sure we save the password details only after the user instance is saved."""
    # test that instance has an id since save can be called without commit
    if (
        created
        and has_attr_present(instance, "id")
        and user_should_set_password_details_skipping_reset(instance)
    ):
        instance.password_details = ResetPasswordExtra(
            user=instance, password_last_updated_at=today()
        )

    if hasattr(instance, "password_details") and has_attr_present(
        instance.password_details, "user_id"
    ):
        instance.password_details.save()


@receiver(pre_save, sender=User)
def set_last_password_update(sender, **kwargs):
    user = kwargs.get("instance")

    if user:
        new_password = user.password
        old_password = find_password_from_db(user)

        if (
            new_password != old_password
            or user_should_set_password_details_skipping_reset(user)
        ):
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
