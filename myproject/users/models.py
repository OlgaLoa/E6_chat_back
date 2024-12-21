from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='', default='default.jpg')

    def __str__(self):
        return self.username


class Room(models.Model):
    room_name = models.CharField(max_length=128, unique=True)
    members = models.ManyToManyField(User, related_name="this_room", blank=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True )

    def __str__(self):
        return self.text
