from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics

from .models import User, Country, Airport, Airline, Airplane, Flight, Ticket
from .serializers import (
    UserSerializer, CountrySerializer, AirportSerializer,
    AirlineSerializer, AirplaneSerializer, FlightSerializer, TicketSerializer, RegisterSerializer
)

@extend_schema(tags=['Authentication'])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

class CustomLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer

    @extend_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(tags=['Users']),
    retrieve=extend_schema(tags=['Users']),
    create=extend_schema(tags=['Users']),
    update=extend_schema(tags=['Users']),
    partial_update=extend_schema(tags=['Users']),
    destroy=extend_schema(tags=['Users']),
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema_view(
    list=extend_schema(tags=['Countries']),
    retrieve=extend_schema(tags=['Countries']),
    create=extend_schema(tags=['Countries']),
    update=extend_schema(tags=['Countries']),
    partial_update=extend_schema(tags=['Countries']),
    destroy=extend_schema(tags=['Countries']),
)
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

@extend_schema_view(
    list=extend_schema(tags=['Airports']),
    retrieve=extend_schema(tags=['Airports']),
    create=extend_schema(tags=['Airports']),
    update=extend_schema(tags=['Airports']),
    partial_update=extend_schema(tags=['Airports']),
    destroy=extend_schema(tags=['Airports']),
)
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related('country').all()
    serializer_class = AirportSerializer

@extend_schema_view(
    list=extend_schema(tags=['Airlines']),
    retrieve=extend_schema(tags=['Airlines']),
    create=extend_schema(tags=['Airlines']),
    update=extend_schema(tags=['Airlines']),
    partial_update=extend_schema(tags=['Airlines']),
    destroy=extend_schema(tags=['Airlines']),
)
class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.select_related('airport').all()
    serializer_class = AirlineSerializer

@extend_schema_view(
    list=extend_schema(tags=['Airplanes']),
    retrieve=extend_schema(tags=['Airplanes']),
    create=extend_schema(tags=['Airplanes']),
    update=extend_schema(tags=['Airplanes']),
    partial_update=extend_schema(tags=['Airplanes']),
    destroy=extend_schema(tags=['Airplanes']),
)
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related('airline').all()
    serializer_class = AirplaneSerializer

@extend_schema_view(
    list=extend_schema(tags=['Flights']),
    retrieve=extend_schema(tags=['Flights']),
    create=extend_schema(tags=['Flights']),
    update=extend_schema(tags=['Flights']),
    partial_update=extend_schema(tags=['Flights']),
    destroy=extend_schema(tags=['Flights']),
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related('origin', 'destination', 'airplane').all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['origin', 'destination', 'status', 'airplane']
    permission_classes = [IsAuthenticated]

@extend_schema_view(
    list=extend_schema(tags=['Tickets']),
    retrieve=extend_schema(tags=['Tickets']),
    create=extend_schema(tags=['Tickets']),
    update=extend_schema(tags=['Tickets']),
    partial_update=extend_schema(tags=['Tickets']),
    destroy=extend_schema(tags=['Tickets']),
)
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('flight', 'user').all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['flight', 'user', 'status']
    permission_classes = [IsAuthenticated]