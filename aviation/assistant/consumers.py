import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from assistant.llm_client import AIService

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        self.service = AIService(user=self.user)
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f"Connected as {getattr(self.user, 'username', 'anonymous')}"
        }))

    async def receive(self, text_data):
        try:
            payload = json.loads(text_data)
            user_msg = payload.get('message') or payload.get('prompt') or ""

            await self.send(text_data=json.dumps({
                'type': 'chat',
                'role': 'user',
                'message': user_msg
            }))

            from asgiref.sync import sync_to_async
            chat_answer = await sync_to_async(self.service.get_response)(user_msg)

            await self.send(text_data=json.dumps({
                'type': 'chat',
                'role': 'bot',
                'message': chat_answer
            }))
        except Exception as e:
            logger.error(f"WS receive error: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"An error occurred: {e}"
            }))