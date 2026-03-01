from rest_framework import serializers
from .models import Country, Airport, Airline, Airplane, Flight, Ticket


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class AirportSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source='country', write_only=True
    )

    class Meta:
        model = Airport
        fields = ['id', 'name', 'iata_code', 'country', 'country_id', 'latitude', 'longitude']


class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    origin_name = serializers.CharField(source='origin.name', read_only=True)
    origin_iata = serializers.CharField(source='origin.iata_code', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_iata = serializers.CharField(source='destination.iata_code', read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'number', 'origin', 'destination',
            'origin_name', 'origin_iata', 'destination_name', 'destination_iata',
            'departure_time', 'arrival_time', 'airplane', 'status',
        ]


class FlightMiniSerializer(serializers.ModelSerializer):
    """Compact flight info for embedding inside ticket responses."""
    origin_iata = serializers.CharField(source='origin.iata_code', read_only=True)
    destination_iata = serializers.CharField(source='destination.iata_code', read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id', 'number', 'origin_iata', 'destination_iata',
            'departure_time', 'arrival_time', 'status',
        ]


class TicketSerializer(serializers.ModelSerializer):
    flight_info = FlightMiniSerializer(source='flight', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'seat_number', 'price', 'status', 'flight', 'order', 'flight_info']
        read_only_fields = ['order']