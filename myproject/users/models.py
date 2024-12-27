from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='', null=True, blank=True )

    def __str__(self):
        return self.username


class Room(models.Model):
    room_name = models.CharField(max_length=128, null=False, blank=False, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms") # владелец = создатель комнаты
    current_users = models.ManyToManyField(User, related_name="current_rooms", blank=True) #участники комнаты
    is_private = models.BooleanField(default=False)  # Новое поле для обозначения личного чата #приватная или нет

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True )

    def __str__(self):
        return self.text
