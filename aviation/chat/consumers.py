import json
from channels.generic.websocket import AsyncWebsocketConsumer
from llm.services.gemini import stream_response

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