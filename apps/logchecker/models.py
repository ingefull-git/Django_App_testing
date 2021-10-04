from django import contrib
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from datetime import datetime as dt
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

SERVERS = ["4-1", "4-2", "4-3", "4-4", "5-1", "5-2", "6-1", "6-2"]
STATUS = (("Error", "Error"), ("Warning", "Warning"), ("Undefined", "Undefined"), ("Ok", "Ok"))



# class UserProfile(models.Model):
#     profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_img = models.ImageField(default='images/default_user_img.png')


class District(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    psid = models.IntegerField(primary_key=True)
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Undefined")
    server = models.CharField(max_length=6, blank=True, null=True)
    psid_str = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f'{self.name} PSID: {self.psid}'

    def toJSON(self):
        item = model_to_dict(self)
        return item
    
    def save(self, *args, **kwargs):
        self.psid_str = f'{self.psid}'
        super().save(*args, **kwargs)

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
    created = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.client} - {self.entity_name}'

    def save(self, *args, **kwargs):
        if self.pk:
            print("UPDATE_Log: ", self.pk)
        if not self.pk:
            print("SAVE_Log: ", self.pk)
        super().save(*args, **kwargs)


class ClientHistoric(models.Model):
    histo = models.CharField(max_length=100, primary_key=True)
    client = models.ForeignKey(District, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length = 40)
    
    def __str__(self) -> str:
        return f'{self.client}_{self.date}_{self.status}'
    
    def save(self, *args, **kwargs):
        if not self.histo:
            client = District.objects.get(pk=self.client)
            self.status = client.status
            datenow = dt.now().date()
            print("DATE: ", datenow)
            self.histo = f'{datenow}_{self.client}'
        return super().save(*args, **kwargs)
