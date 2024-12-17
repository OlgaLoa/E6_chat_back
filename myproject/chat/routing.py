# необходимо сначала настроить маршрутизацию.
# Это включает в себя определение путей, по которым клиенты могут подключаться
# к вашему серверу через WebSockets.
# В этом файле вы будете определять пути WebSocket.
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]


# re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),