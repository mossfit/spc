import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dashboard_updates"
        # Join dashboard group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave dashboard group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def dashboard_update(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
