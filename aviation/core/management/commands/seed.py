from core.models import Country, Airport, Airline, Flight, Ticket, Airplane
from django.utils.timezone import now, timedelta
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed database with initial test data"

    def handle(self, *args, **options):
        # Countries
        ua, _ = Country.objects.get_or_create(name="Ukraine", code="UA")
        pl, _ = Country.objects.get_or_create(name="Poland", code="PL")

        # Airports
        lwo, _ = Airport.objects.get_or_create(name="Lviv Airport", iata_code="LWO", country=ua)
        krk, _ = Airport.objects.get_or_create(name="Krakow Airport", iata_code="KRK", country=pl)

        # Airlines
        sky, _ = Airline.objects.get_or_create(name="SkyUp Airlines", code="SU", airport=lwo)
        lot, _ = Airline.objects.get_or_create(name="LOT Polish Airlines", code="LO", airport=krk)

        # Airplanes
        plane1, _ = Airplane.objects.get_or_create(
            model="Boeing 737",
            airline=sky,
            seats_count=180,
            registration="UR-SKY001"
        )

        plane2, _ = Airplane.objects.get_or_create(
            model="Embraer 190",
            airline=lot,
            seats_count=120,
            registration="SP-LOT001"
        )

        # Flights
        flight, _ = Flight.objects.update_or_create(
            number="TA123",
            defaults={
                "origin": lwo,
                "destination": krk,
                "airplane": plane1,
                "departure_time": now() + timedelta(days=1),
                "arrival_time": now() + timedelta(days=1, hours=2),
                "status": "scheduled",
            }
        )

        # Tickets
        Ticket.objects.get_or_create(flight=flight, seat_number="1A", price=100, status="available")
        Ticket.objects.get_or_create(flight=flight, seat_number="1B", price=100, status="available")
        Ticket.objects.get_or_create(flight=flight, seat_number="2A", price=120, status="booked")

        self.stdout.write(self.style.SUCCESS("✅ Seed data created successfully!"))