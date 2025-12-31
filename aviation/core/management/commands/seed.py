from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Country, Airport, Airline, Airplane, Flight, Ticket

class Command(BaseCommand):
    help = "Seed test flight Lviv -> Krakow for tomorrow"

    def handle(self, *args, **options):
        tomorrow = timezone.now() + timedelta(days=1)

        # Countries
        ukraine, _ = Country.objects.get_or_create(
            code="UA",
            defaults={"name": "Ukraine"}
        )
        poland, _ = Country.objects.get_or_create(
            code="PL",
            defaults={"name": "Poland"}
        )

        # Airports (ось тут твій код 👇)
        lviv_airport, _ = Airport.objects.get_or_create(
            iata_code="LWO",
            defaults={"name": "Lviv", "country": ukraine}
        )
        krakow_airport, _ = Airport.objects.get_or_create(
            iata_code="KRK",
            defaults={"name": "Krakow", "country": poland}
        )

        # Airline
        airline, _ = Airline.objects.get_or_create(
            code="TA123",
            defaults={"name": "TestAir", "airport": lviv_airport}
        )

        # Airplane
        airplane, _ = Airplane.objects.get_or_create(
            registration="UR-TEST",
            defaults={"model": "Boeing 737", "seats_count": 180, "airline": airline}
        )

        # Flight
        flight, created = Flight.objects.get_or_create(
            number="TA1001",
            defaults={
                "origin": lviv_airport,
                "destination": krakow_airport,
                "departure_time": tomorrow.replace(hour=10, minute=0, second=0, microsecond=0),
                "arrival_time": tomorrow.replace(hour=11, minute=0, second=0, microsecond=0),
                "airplane": airplane,
                "status": Flight.Status.SCHEDULED,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS("✅ Flight Lviv -> Krakow created"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Flight already exists"))

        # Tickets
        for seat in ["1A", "1B", "2A", "2B"]:
            Ticket.objects.get_or_create(
                flight=flight,
                seat_number=seat,
                defaults={"price": 120.00, "status": "available"}
            )

        self.stdout.write(self.style.SUCCESS("🎫 Tickets created"))