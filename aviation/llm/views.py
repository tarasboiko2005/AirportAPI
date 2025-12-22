from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .services.gemini import RoadmapGenerator
from .serializers import RoadmapInputSerializer

class RoadmapView(APIView):
    @extend_schema(
        request=RoadmapInputSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "skills": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "category": {"type": "string"},
                                "difficulty": {"type": "integer"},
                                "description": {"type": "string"}
                            }
                        }
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "from": {"type": "string"},
                                "to": {"type": "string"},
                                "type": {"type": "string", "enum": ["hard", "soft"]}
                            }
                        }
                    }
                }
            },
            400: {"type": "object", "properties": {"detail": {"type": "string"}}},
            500: {"type": "object", "properties": {"detail": {"type": "string"}}}
        },
        description="Generates a learning roadmap by topic via LLM (Gemini API)"
    )
    def post(self, request):
        serializer = RoadmapInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data["topic"]

        try:
            generator = RoadmapGenerator()
            data = generator.generate(topic)
            return Response(data, status=200)

        except Exception as e:
            return Response({"detail": f"LLM error: {str(e)}"}, status=400)
