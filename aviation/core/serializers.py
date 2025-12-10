from rest_framework import serializers
from .models import Country, Airport, Airline, Airplane, Flight, Ticket

class CountrySerializer(serializers.ModelSerializer):
    class Meta: model = Country; fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )
    class Meta: model = Airport; fields = ['id','name','iata_code','country','country_id']

class AirlineSerializer(serializers.ModelSerializer):
    class Meta: model = Airline; fields = '__all__'

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta: model = Airplane; fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta: model = Flight; fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'seat_number', 'price', 'status', 'flight', 'order']
        read_only_fields = ['order']