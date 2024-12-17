# Определите класс Consumer, который будет управлять WebSocket соединениями.
# когда Channels принимает соединение WebSocket, он проверяет конфигурацию корневой маршрутизации
# для поиска потребителя, а затем вызывает различные функции потребителя для обработки событий
# из соединения

# это синхронный потребитель WebSocket, который принимает все соединения, получает сообщения
# от своего клиента и отправляет эти сообщения обратно тому же клиенту.
# На данный момент он не передает сообщения другим клиентам в той же комнате.
# На данный момент он не передает сообщения другим клиентам в той же комнате.

# В нашем приложении чата мы хотим, чтобы несколько экземпляров ChatConsumer общались друг с другом в одной комнате.
# Для этого каждый ChatConsumer добавит свой канал в группу, имя которой основано на названии комнаты.
# Это позволит ChatConsumers передавать сообщения всем остальным ChatConsumers в той же комнате.

# Мы будем использовать слой канала, который использует Redis в качестве резервного хранилища.

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Добавьте здесь логику при отключении

    async def receive(self, text_data):
        text_data_json = json.loads(text_data) #loads преобразует строку в формате JSON в объект Python
        message = text_data_json['message']
        await self.send(text_data=json.dumps({ #Функция dumps() модуля json сериализирует объект Python obj в строку str формата JSON
            'message': message
        }))