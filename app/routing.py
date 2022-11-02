from django.urls import path
from . import consumers
from . import views

websocket_urlpathterns = [
    path('ws/socket-server/<str:groupkaname>/', consumers.ChatConsumer.as_asgi()),

    # path('chat_login/', views.chat_login, name='chat_login'),
]
