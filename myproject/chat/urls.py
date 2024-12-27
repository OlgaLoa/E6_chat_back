from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # WebS функция присоединения к чату по названию
    path('chat/', views.index, name='index'),

    # функция просмотра для комнаты, которое позволяет видеть сообщения, опубликованные в определенной комнате чата (для приватного и общего)
    path('chat/<str:room_name>/', views.room, name='room'),

    #вызов функции создания приватного чата с передаваемым id юзера ( формируется навание компаны из айди юзеров)
    path('create_private_chat/<int:user_id>/', views.create_private_chat, name='create_private_chat'),

    #вызов функции создания общего чата с передаваемым названием чата
    path('create_public_chat/<str:room_name>/', views.create_public_chat, name='create_public_chat'),

    path('chat_list/', ChatList.as_view(), name='room_list'),
    path('chat_update/<int:pk>/', ChatUpdate.as_view(), name='room_update'),
    path('chat_delete/<int:pk>/', ChatDelete.as_view(), name='room_delete'),
]


