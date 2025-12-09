from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404
import logging

from .models import Country, Airport, Airline, Airplane, Flight, Ticket
from .serializers import (
    CountrySerializer, AirportSerializer,
    AirlineSerializer, AirplaneSerializer, FlightSerializer, TicketSerializer
)

logger = logging.getLogger(__name__)

# Country through Generics Views
@extend_schema(tags=['Countries'])
class CountryListCreateView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@extend_schema(tags=['Countries'])
class CountryDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk=pk, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk=pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        return self.partial_update(request, pk=pk, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, pk=pk, *args, **kwargs)

# Airport through Generic Views
@extend_schema(tags=['Airports'])
class AirportListCreateView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Airport.objects.select_related('country').all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@extend_schema(tags=['Airports'])
class AirportDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = Airport.objects.select_related('country').all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk=pk, *args, **kwargs)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk=pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        return self.partial_update(request, pk=pk, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, pk=pk, *args, **kwargs)

# Airlines through APIView
@extend_schema(tags=['Airlines'])
class AirlineListView(APIView):
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        airlines = Airline.objects.all()
        serializer = AirlineSerializer(airlines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AirlineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Airlines'])
class AirlineDetailView(APIView):
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        airline = get_object_or_404(Airline, pk=pk)
        serializer = AirlineSerializer(airline)
        return Response(serializer.data)

    def put(self, request, pk):
        airline = get_object_or_404(Airline, pk=pk)
        serializer = AirlineSerializer(airline, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        airline = get_object_or_404(Airline, pk=pk)
        serializer = AirlineSerializer(airline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        airline = get_object_or_404(Airline, pk=pk)
        airline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Flights through ViewSet
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

#Tickets through APIView
@extend_schema(tags=['Tickets'])
class TicketListView(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tickets = Ticket.objects.select_related('flight', 'order').all()
        serializer = self.serializer_class(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Ticket created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Ticket creation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Tickets'])
class TicketDetailView(APIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = self.serializer_class(ticket)
        return Response(serializer.data)

    def put(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = self.serializer_class(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = self.serializer_class(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Airplane through viewset
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