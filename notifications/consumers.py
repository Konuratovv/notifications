from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('notifications', self.channel_name)
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard('notifications', self.channel_name)
        
    async def send_notifications(self, event):
        message = event['message']

        await self.send(
            text_data = json.dumps({
                "type": "notification",
                "message": message,
            }
            )
        )