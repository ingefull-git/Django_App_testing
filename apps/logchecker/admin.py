from django.contrib import admin
from apps.logchecker.models import District, Log, ClientHistoric


admin.site.register(District)
admin.site.register(Log)
admin.site.register(ClientHistoric)


