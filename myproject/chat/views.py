from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from users.models import *
from .serializers import *
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Индексное представление, которое позволяет ввести имя комнаты = чата, чтобы присоединиться.
def index(request):
    return render(request, 'chat/index.html')#передаем данные запроса в форму


# функция создания личного чата (комната). При создании личного чата комната будет называться по сочетанию двух пользователей, чтобы поддерживать уникальность.
# Эта функция проверит наличие чата и создаст его, если он не существует.
def create_private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    room_name = f"{request.user.id}_{other_user.id}"  #При создании личного чата комната будет называться по сочетанию двух пользователей

    # Проверка, существует ли уже чат между пользователями
    room, created = Room.objects.get_or_create( # или создаем объект чата (комнаты), если уже не существует такая
        room_name=room_name,
        defaults={'host': request.user, 'is_private': True}
    )
    room.current_users.add(request.user, other_user) #добавляем пользователей в объект комнаты как current_users
    return redirect('room', room_name=room.room_name, ) #перенаправляем на функция создания чата, передавая туда сформированное название приватной комнаты

#функцию просмотра для комнаты(для приватного и общего)
def room(request, room_name):
    return render(request, 'chat/room.html', {   # 'chat/room.html' - одинаковый для приватного и общего чата
        'room_name': room_name
    })

# функция создания общего чата (комната).
def create_public_chat(request, room_name):
    room, created = Room.objects.get_or_create( #поиск существующей записи в модели или создания новой в случае её отсутствия:
        # Этот метод возвращает кортеж (object, created), где object — это найденный или созданный экземпляр модели,
        # а created — булевая переменная, указывающая на создание объекта (True) или его извлечение из базы данных (False).
        room_name=room_name,
        defaults={'host': request.user, 'is_private': False}
    )
    room.current_users.add(request.user)

    # перенаправляем на функция создания чата, передавая туда сформированное название общей комнаты
    return render(request, 'chat/room.html', {  # 'chat/room.html' - одинаковый для приватного и общего чата
        'room_name': room_name
    })


# СПИСОК ЧАТОВ (КОМНАТ)
class ChatList(ListView):
    model = Room
    template_name = 'chat/room_list.html'
    context_object_name = 'room_list'

# ИЗМЕНИТЬ ЧАТ (КОМНАТУ)
class ChatUpdate(UpdateView): #без отдельной формы
    model = Room
    fields = ['room_name', 'host']
    template_name = 'chat/room_update.html'
    success_url = reverse_lazy('room')


# УДАЛИТЬ ЧАТ (КОМНАТУ)
class ChatDelete(DeleteView):
    model = Room
    template_name = 'chat/room_delete.html'
    success_url = '/chat/'











