from django.urls import path
from console import views

app_name = 'console'
urlpatterns = [
    path('', views.index, name='index'),
    path('shadowsocks', views.shadowsocks, name='shadowsocks'),
]
