from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from assistant.llm_client import AIService

@extend_schema(
    tags=["LLM"],
    summary="Natural language query to AirportAPI",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "example": "Show flights from Lviv to Krakow tomorrow"},
                "lang": {"type": "string", "example": "en"}
            },
            "required": ["prompt"]
        }
    },
    responses={
        200: OpenApiResponse(description="Success response with structured data"),
        400: OpenApiResponse(description="Invalid or unknown action"),
        500: OpenApiResponse(description="LLM error or internal failure"),
    },
)
class NaturalLanguageQueryView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"status": "error", "message": "Missing prompt"}, status=400)

        try:
            service = AIService(user=request.user)
            answer = service.get_response(prompt)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)

        return Response({"status": "success", "message": "Success", "data": answer}, status=200)