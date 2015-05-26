from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    username = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    name = models.CharField(_('Name'), max_length=256)

    def __str__(self):
        return self.name



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.username = instance.username
        profile.email = instance.email
        profile.name = ' '.join([instance.first_name, instance.last_name])
        profile.save()

post_save.connect(create_user_profile, sender=User)
