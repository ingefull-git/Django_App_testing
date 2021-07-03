from django.urls import path
from . import views

app_name = 'logchecker'

urlpatterns = [
    path('', views.home, name='home'),
]