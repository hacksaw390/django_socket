from email import message
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Group, Chat
from channels.db import database_sync_to_async

class ChatConsumer(WebsocketConsumer):

    
    def connect(self):
        
        print('websocket connected')
        print('layer-------', self.channel_layer)
        print('name---------', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('group name==============',self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()
    
    def receive(self, text_data):
        print('messsage received:==============', text_data)
        try:
            data = json.loads(text_data)
            message = data['message']
            print(message)


            group = Group.objects.get(name= self.group_name)
            chat = Chat(
                content = data['message'],
                group = group
            )
            chat.save()

            
            async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message': message
            }
            )
            
        except:
            print("An exception occurred")

       
    def chat_message(self, event):
        message = event['message']
        print('============================', message)

        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message
        }))
        
        

class AsyncChatConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        
        print('websocket connected')
        print('layer-------', self.channel_layer)
        print('name---------', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('group name==============',self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def receive(self, text_data):
        print('messsage received:==============', text_data)
        try:
            data = json.loads(text_data)
            message = data['message']
            print(message)


            group = await database_sync_to_async(Group.objects.get)(name= self.group_name)
            chat = Chat(
                content = data['message'],
                group = group
            )
            await database_sync_to_async(chat.save)()
            
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message',
                'message': message
            }
            )
            
        except:
            print("An exception occurred")

       
    async def chat_message(self, event):
        message = event['message']
        print('============================', message)

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message': message
        }))

    