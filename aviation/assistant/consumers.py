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
            'message': f"<p>Connected as <b>{getattr(self.user, 'username', 'anonymous')}</b></p>"
        }))

    async def receive(self, text_data):
        try:
            payload = json.loads(text_data)
            user_msg = payload.get('message') or payload.get('prompt') or ""

            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': f"<p>You: {user_msg}</p>"
            }))

            from asgiref.sync import sync_to_async
            chat_answer = await sync_to_async(self.service.get_response)(user_msg)

            await self.send(text_data=json.dumps({
                'type': 'chat',
                'message': f"<p>Chat: {chat_answer}</p>"
            }))
        except Exception as e:
            logger.error(f"WS receive error: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"<p>Error: {e}</p>"
            }))