from rest_framework import viewsets
from .models import User, Country, Airport, Airline, Airplane, Flight, Ticket
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer, CountrySerializer, AirportSerializer,
    AirlineSerializer, AirplaneSerializer, FlightSerializer, TicketSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related('country').all()
    serializer_class = AirportSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.select_related('airport').all()
    serializer_class = AirlineSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related('airline').all()
    serializer_class = AirplaneSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related('origin','destination','airplane').all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin', 'destination', 'status', 'airplane']
    permission_classes = [IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('flight','user').all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight', 'user', 'status']
    permission_classes = [IsAuthenticated]