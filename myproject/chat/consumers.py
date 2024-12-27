# In Django Channels, the consumer enables you to create sets of functions in your code that will be called whenever an event occurs. They are similar to views in Django.

# Определите класс Consumer, который будет управлять WebSocket соединениями.
# когда Channels принимает соединение WebSocket, он проверяет конфигурацию корневой маршрутизации
# для поиска потребителя, а затем вызывает различные функции потребителя для обработки событий из соединения

# Мы будем использовать слой канала, который использует Redis в качестве резервного хранилища.

# Канальный уровень - это своего рода система связи. Это позволяет нескольким пользовательским экземплярам общаться друг с другом и с другими частями Django.
# Канальный уровень предоставляет следующие абстракции:
# Канал - это почтовый ящик, куда можно отправлять сообщения. У каждого канала есть имя. Любой, у кого есть название канала, может отправить сообщение на канал.
# Группа - это группа связанных каналов. У группы есть имя. Любой, у кого есть имя группы, может добавить/удалить канал в группе по имени и отправить сообщение всем каналам в группе. Невозможно перечислить, какие каналы находятся в определенной группе.
# Каждый потребительский экземпляр имеет автоматически сгенерированное уникальное имя канала, поэтому с ним можно связаться через уровень канала.
# В нашем приложении чата мы хотим, чтобы несколько экземпляров ChatConsumer общались друг с другом в одной комнате. Для этого каждый ChatConsumer добавит свой канал в группу, имя которой основано на названии комнаты. Это позволит ChatConsumers передавать сообщения всем остальным ChatConsumers в той же комнате.

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Когда пользователь отправляет сообщение, функция JavaScript передает сообщение через WebSocket в ChatConsumer.
# ChatConsumer получит это сообщение и отправит его группе, соответствующей названию комнаты. Каждый ChatConsumer в той же группе
# (и, следовательно, в той же комнате) получит сообщение от группы и перенаправит его через WebSocket обратно в JavaScript,
# где оно будет добавлено в журнал чата.
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #Получает параметр 'room_name' из URL-маршрута в chat/routing.py, который открывает соединение WebSocket с потребителем (re_path(r'ws/chat/(?P<room_name>\w+)/$')
        # У каждого потребителя есть область видимости, которая содержит информацию о его соединении, включая, в частности, любые позиционные или ключевые аргументы из URL-маршрута и текущего аутентифицированного пользователя, если таковой имеется.

        self.room_group_name = 'chat_%s' % self.room_name #Создает имя группы каналов непосредственно из указанного пользователем номера комнаты, без кавычек или экранирования.

        # Join room group
        await self.channel_layer.group_add( #Декоратор async_to_sync(…) требуется, потому что ChatConsumer является синхронным WebsocketConsumer, но он вызывает метод асинхронного канального уровня. (Все методы канального уровня являются асинхронными.)
            self.room_group_name,
            self.channel_name
        )

        await self.accept() #Принимает соединение WebSocket. Рекомендуется, чтобы accept() был вызван как последнее действие в connect(), если вы решите принять соединение.

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send( #Отправляет событие в группу.
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


# ChatConsumer теперь наследуется от AsyncWebsocketConsumer, а не от WebsocketConsumer.
# Все методы являются async def, а не просто def.
# await используется для вызова асинхронных функций, которые выполняют ввод/вывод.
# async_to_sync больше не требуется при вызове методов на канальном уровне.