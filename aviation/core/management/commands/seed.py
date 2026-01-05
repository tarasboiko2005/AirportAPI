from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from core.models import Country, Airport, Airline, Airplane, Flight, Ticket, Order

User = get_user_model()

class Command(BaseCommand):
    help = "Seed test data: flights Lviv -> Krakow with tickets and orders"

    def handle(self, *args, **options):
        now = timezone.now()

        # Countries
        ukraine, _ = Country.objects.get_or_create(
            code="UA", defaults={"name": "Ukraine"}
        )
        poland, _ = Country.objects.get_or_create(
            code="PL", defaults={"name": "Poland"}
        )

        # Airports
        lviv_airport, _ = Airport.objects.get_or_create(
            iata_code="LWO", defaults={"name": "Lviv", "country": ukraine}
        )
        krakow_airport, _ = Airport.objects.get_or_create(
            iata_code="KRK", defaults={"name": "Krakow", "country": poland}
        )

        # Airline
        airline, _ = Airline.objects.get_or_create(
            code="TA123", defaults={"name": "TestAir", "airport": lviv_airport}
        )

        # Airplane
        airplane, _ = Airplane.objects.get_or_create(
            registration="UR-TEST",
            defaults={"model": "Boeing 737", "seats_count": 180, "airline": airline},
        )

        # User for orders
        user, _ = User.objects.get_or_create(
            email="tarasboiko2005@gmail.com",
            defaults={"username": "taras", "password": "test1234"}
        )

        # Flights for today, tomorrow, day after
        for offset in range(3):
            departure = now + timedelta(days=offset)
            flight, created = Flight.objects.get_or_create(
                number=f"TA100{offset}",
                origin=lviv_airport,
                destination=krakow_airport,
                departure_time=departure.replace(hour=10, minute=0, second=0, microsecond=0),
                arrival_time=departure.replace(hour=11, minute=0, second=0, microsecond=0),
                airplane=airplane,
                status=Flight.Status.SCHEDULED,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Flight {flight.number} created"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Flight {flight.number} already exists"))

            # Tickets (some available, some booked)
            seats = ["1A", "1B", "2A", "2B"]
            for i, seat in enumerate(seats):
                ticket, _ = Ticket.objects.get_or_create(
                    flight=flight,
                    seat_number=seat,
                    defaults={"price": 120.00, "status": "available"},
                )
                # Mark some tickets as booked
                if i % 2 == 1:  # every second seat booked
                    ticket.status = "booked"
                    ticket.save()
                    # Create order for booked ticket
                    Order.objects.get_or_create(
                        user=user,
                        ticket=ticket,
                        defaults={"status": "confirmed"}
                    )

            self.stdout.write(self.style.SUCCESS(f"🎫 Tickets + Orders for {flight.number} created"))