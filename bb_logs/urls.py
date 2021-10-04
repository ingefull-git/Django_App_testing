from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.logchecker.urls', namespace="logchecker")),
    path('', include('apps.login.urls', namespace="login")),
    path('api/', include('apps.restapi.urls', namespace="restapi")),
    path('accounts/', include('allauth.urls')),
]
