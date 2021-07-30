from django import contrib
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict

SERVERS = ["4-1", "4-2", "4-3", "4-4", "5-1", "5-2", "6-1", "6-2"]
STATUS = (("Error", "Error"), ("Warning", "Warning"), ("Undefined", "Undefined"), ("Ok", "Ok"))

class UserProfile(models.Model):
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='images/default_user_img.png')


class District(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    psid = models.IntegerField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Undefined")
    server = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f'{self.name} PSID: {self.psid} - {self.status}'

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ['psid']


class Log(models.Model):
   
    entity_name = models.CharField(max_length=20, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    client = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=True, null=True)

    def __str__(self):
        return f'{self.client} - {self.entity_name}_{self.status}'

    def save(self, *args, **kwargs):
        if self.pk:
            print("UPDATE_Log: ", self.pk)
        if not self.pk:
            print("SAVE_Log: ", self.pk)
        super().save(*args, **kwargs)
