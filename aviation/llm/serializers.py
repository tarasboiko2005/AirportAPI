from rest_framework import serializers
from core.serializers import CountrySerializer, AirportSerializer, AirlineSerializer, AirplaneSerializer
from core.models import Flight, Ticket

class FlightLLMSerializer(serializers.ModelSerializer):
    origin = AirportSerializer()
    destination = AirportSerializer()
    airplane = AirplaneSerializer()
    flight_status = serializers.CharField(source="status")

    class Meta:
        model = Flight
        fields = [
            "number",
            "origin",
            "destination",
            "departure_time",
            "arrival_time",
            "airplane",
            "flight_status",
        ]
        ref_name = "LLMFlight"

class LlmTicketSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(source="flight.number", read_only=True)
    ticket_status = serializers.CharField(source="status")

    class Meta:
        model = Ticket
        fields = ["seat_number", "price", "ticket_status", "flight_number"]
        ref_name = "LLMTicket"

class LlmResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()
    data = serializers.ListField()

