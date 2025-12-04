from rest_framework import serializers
from .models import User, Country, Airport, Airline, Airplane, Flight, Ticket

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        def validate_username(self, value):
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("This username is already in use.")
            return value

        def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
            return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta: model = User; fields = ['id','username','email','role']

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
    class Meta: model = Ticket; fields = '__all__'