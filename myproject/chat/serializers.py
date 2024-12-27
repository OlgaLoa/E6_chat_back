# при реализации API сайта обмен данными выполняется посредством определенного формата. Чаще всего используют JSON

# роль сериализатора выполнять конвертирование произвольных объектов языка Python в формат JSON
# (в том числе модели фреймворка Django и наборы QuerySet). И, обратно, из JSON – в соответствующие объекты Python. (

# хорошей практикой считается, когда здесь же в сериализаторе определяется алгоритм сохранения или изменения данных в БД

from rest_framework import serializers
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User #модель, с которой должен работать данный сериализатор
        fields = ('username', 'date_joined') #набор полей таблицы (атрибутов модели) для сериализации


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_name', 'members')