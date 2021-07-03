from django import contrib
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='images/default_user_img.png')

@receiver(post_save, sender=User)
def update_user_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(profile_user=instance)
    instance.userprofile.save()


class District(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    psid = models.IntegerField(null=True, blank=True)
    crated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} PSID: {self.psid}'
