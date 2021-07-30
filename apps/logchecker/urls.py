from django.urls import path
from . import views

app_name = 'logchecker'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('read_log/<int:psid>/', views.update_log_view, name='readlog'),
    path('chart_detail/<str:label>/', views.chart_detail_view, name='chartdetail'),
    path('district/<int:psid>/update/', views.update_view, name='district_update'),
    path('district/new/', views.create_view, name='district_new')
]