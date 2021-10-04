from django.urls import path
from apps.restapi import views
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'restapi'

urlpatterns = [
    # path('', views.ClientListView.as_view(), name='client-list'),
    path('', views.UserAccountListAPIView.as_view(), name='useraccount-list'),
    # path('', views.useraccountlistapiview, name='useraccount-list'),
    path('register', views.registerview, name='register'),
    # path('login', obtain_auth_token, name='login'),
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('<int:pk>/detail/', views.ClientDetailView.as_view(), name='client-detail'),
    path('get-update/', views.get_update_useraccountapiview, name='useraccount-get-update'),
]