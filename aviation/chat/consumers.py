import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder

from llm.services.gemini import stream_response
from llm.queries import execute

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            msg_type = data.get("type")
            payload = data.get("payload", {})

            if msg_type == "user_message":
                action = payload.get("action")
                params = payload.get("params", {})

                if action:
                    result = await database_sync_to_async(execute)(action, params)

                    if hasattr(result, "values"):
                        result = list(result.values())

                    await self.send(text_data=json.dumps({
                        "type": "db_result",
                        "payload": result
                    }, cls=DjangoJSONEncoder))

                else:
                    prompt = payload.get("text", "")
                    async for chunk in stream_response(prompt):
                        await self.send(text_data=json.dumps({
                            "type": "assistant_chunk",
                            "payload": {"text": chunk}
                        }))
                    await self.send(text_data=json.dumps({
                        "type": "assistant_complete",
                        "payload": {"done": True}
                    }))

            elif msg_type == "ping":
                await self.send(text_data=json.dumps({"type": "pong"}))

            else:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "payload": {"message": "Unknown message type"}
                }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                "type": "error",
                "payload": {"message": f"Error: {str(e)}"}
            }))