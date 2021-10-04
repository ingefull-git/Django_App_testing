from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('login/', views.loginview, name='login-view'),
    path('logout/', views.logoutview, name='logout-view'),
]
