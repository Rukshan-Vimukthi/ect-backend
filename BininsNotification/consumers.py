from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from django.contrib.auth.models import User
        user = self.scope["user"]
        self.group_name = ""
        if isinstance(user, User):
            if user.is_superuser:
                self.group_name = "adminNotificationUpdate"
            else:
                self.group_name = f"{user.username}-{user.id}"
                
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close(code=4001)
            return

    async def disconnect(self, code):
        await self.channel_layer.group_discard("adminNotificationUpdate", self.channel_name)

    async def notify(self, information):
        await self.send(text_data=json.dumps(information))
