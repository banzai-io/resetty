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


#  @receiver(post_save, sender=User)
#  def create_user_profile(sender, instance, created, **kwargs):
#      if created:
#          print('Created a new user')
#          #  Profile.objects.create(user=instance)
#      import pdb
#      pdb.set_trace()
#      print("Hallo")
