from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name="lobby"),
    path('home/', views.home, name="home"),
    path('chat_login/', views.chat_login, name='chat_login'),
    path('<str:groupname>/', views.index),
]
