import json
import logging
from channels.generic.websocket import WebsocketConsumer
from assistant.llm_client import AIService

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope.get("user")
        self.service = AIService(user=self.user)
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f"<p>Connected as <b>{getattr(self.user, 'username', 'anonymous')}</b></p>"
        }))

    def receive(self, text_data):
        try:
            payload = json.loads(text_data)
            user_msg = payload.get('message', '')

            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': f"<p>You: {user_msg}</p>"
            }))

            chat_answer = self.service.get_response(user_msg)
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': f"<p>Chat: {chat_answer}</p>"
            }))
        except Exception as e:
            logger.error(f"WS receive error: {e}")
            self.send(text_data=json.dumps({
                'type': 'error',
                'message': f"<p>Error: {e}</p>"
            }))