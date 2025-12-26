from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from llm.llm_client import LLMClient, LLMClientError
from llm.intents import map_intent
from llm.queries import execute

from core.schema import ok, fail
from core.i18n import detect_lang, t
from core.logging import get_logger
from llm.serializers import FlightLLMSerializer, LlmTicketSerializer

logger = get_logger(__name__)

@extend_schema(
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
        200: OpenApiResponse(
            response=FlightLLMSerializer,
            description="Response with flights"
        ),
        201: OpenApiResponse(
            response=LlmTicketSerializer,
            description="Response with tickets"
        ),
        202: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "ok"},
                    "message": {"type": "string", "example": "Success"},
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "example": "Poland"},
                                "code": {"type": "string", "example": "PL"}
                            }
                        }
                    }
                }
            },
            description="Response with countries"
        ),
        203: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "example": "ok"},
                    "message": {"type": "string", "example": "Success"},
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "example": "Ukraine International"},
                                "code": {"type": "string", "example": "PS"}
                            }
                        }
                    }
                }
            },
            description="Response with airlines"
        )
    },
    examples=[
        OpenApiExample(
            name="Basic query",
            value={"prompt": "Show flights from Lviv to Krakow tomorrow", "lang": "en"},
            request_only=True
        ),
        OpenApiExample(
            name="Example response (flights)",
            value={
                "status": "ok",
                "message": "Success",
                "data": [
                    {
                        "number": "PS123",
                        "origin": {"name": "Lviv Airport", "iata_code": "LWO", "country": {"name": "Ukraine", "code": "UA"}},
                        "destination": {"name": "Krakow Airport", "iata_code": "KRK", "country": {"name": "Poland", "code": "PL"}},
                        "departure_time": "2025-12-24T08:00:00Z",
                        "arrival_time": "2025-12-24T09:00:00Z",
                        "airplane": {
                            "registration": "UR-PS123",
                            "model": "Boeing 737",
                            "seats_count": 180,
                            "airline": {
                                "name": "Ukraine International",
                                "code": "PS",
                                "airport": {"name": "Boryspil Airport", "iata_code": "KBP", "country": {"name": "Ukraine", "code": "UA"}}
                            }
                        },
                        "status": "scheduled"
                    }
                ]
            },
            response_only=True
        ),
        OpenApiExample(
            name="Example response (tickets)",
            value={
                "status": "ok",
                "message": "Success",
                "data": [
                    {"seat_number": "12A", "price": "100.00", "status": "available"},
                    {"seat_number": "12B", "price": "120.00", "status": "sold"}
                ]
            },
            response_only=True
        ),
    ],
    tags=["LLM"]
)
class NaturalLanguageQueryView(APIView):
    """
    Endpoint for natural language queries.
    """

    def post(self, request):
        prompt = request.data.get("prompt", "")
        lang = request.data.get("lang") or detect_lang(prompt)

        if not prompt.strip():
            return Response(
                fail(
                    message=t("intent_unknown", lang),
                    errors=["Empty prompt"],
                    lang=lang
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            intent = LLMClient().extract_intent(prompt=prompt, lang=lang)
            intent["prompt"] = prompt
        except LLMClientError as e:
            logger.error(f"LLM error: {e}")
            return Response(
                fail(
                    message=t("intent_unknown", lang),
                    errors=[str(e)],
                    lang=lang
                ),
                status=status.HTTP_502_BAD_GATEWAY
            )

        action, params = map_intent(intent)
        logger.info(f"Mapped action: {action}, params: {params}")

        if action == "unknown":
            return Response(
                fail(
                    message=t("intent_unknown", lang),
                    errors=intent.get("errors", []),
                    lang=lang
                ),
                status=status.HTTP_200_OK
            )

        results = execute(action, params)

        if not results:
            return Response(ok([], t("no_results", lang), lang), status=status.HTTP_200_OK)

        if action in ["search_tickets", "search_available_tickets", "search_booked_tickets"]:
            serializer = LlmTicketSerializer(results, many=True)
        elif action == "search_flights":
            serializer = FlightLLMSerializer(results, many=True)
        elif action in ["search_countries_from_origin", "search_airlines_from_airport"]:
            return Response(ok(results, lang=lang), status=status.HTTP_200_OK)
        else:
            return Response(ok([], t("no_results", lang), lang), status=status.HTTP_200_OK)

        return Response(ok(serializer.data, lang=lang), status=status.HTTP_200_OK)