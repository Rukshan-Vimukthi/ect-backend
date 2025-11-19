from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            user = self.scope["user"]
            self.group_name = None
            session = self.scope["session"]
            email = await sync_to_async(session.get)("email")

            if user and user.is_authenticated:
                # print("WebSocket Chat Consumer: User is authenticated")
                self.group_name = f"{user.username}-chat"
            elif session is not None:
                # print("WebSocket Chat Consumer: User is anonymous")
                # print(email)
                if email:
                    self.group_name = f"{session['email'].replace('@', '-').replace('.', '-')}-chat"

            if self.group_name is not None:
                # print("Group Name: ", self.group_name)
                await self.channel_layer.group_add(self.group_name, self.channel_name)
                await self.accept()
                from .views import getContactList
                contacts = await sync_to_async(getContactList)(user, email)
                print(contacts)
                await self.send(text_data=json.dumps({"contacts": contacts}))
            await self.close()
        except Exception as e:
            print(e)
            # print("Error occurred!")
            await self.close()
    
    async def disconnect(self, code):
        try:
            if self.group_name is not None:
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception as e:
            print(e)
            pass
    
    async def notify(self, message):
        await self.send(text_data=json.dumps({"message": message}))

    async def updateContact(self, message):
        await self.send(text_data=json.dumps(message["message"]))
