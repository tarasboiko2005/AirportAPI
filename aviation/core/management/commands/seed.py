from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, time, datetime, timezone as dt_timezone
from django.contrib.auth import get_user_model
from core.models import Country, Airport, Airline, Airplane, Flight, Ticket
from orders.models import Order

User = get_user_model()


class Command(BaseCommand):
    help = "Seed test data: flights Lviv -> Krakow with tickets, orders, and superuser"

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

        # User (superuser for admin + orders)
        user, created = User.objects.get_or_create(
            email="tarasboiko2005@gmail.com",
            defaults={"username": "taras"}
        )
        if created:
            user.set_password("Qwest2005")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS("✅ Superuser created"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ User already exists"))

        # Flights for today, tomorrow, day after
        for offset in range(3):
            departure_date = (now + timedelta(days=offset)).date()
            departure_dt = datetime.combine(
                departure_date, time(10, 0), tzinfo=dt_timezone.utc
            )
            arrival_dt = datetime.combine(
                departure_date, time(11, 0), tzinfo=dt_timezone.utc
            )

            flight, created = Flight.objects.get_or_create(
                number=f"TA100{offset}",
                origin=lviv_airport,
                destination=krakow_airport,
                defaults={
                    "departure_time": departure_dt,
                    "arrival_time": arrival_dt,
                    "airplane": airplane,
                    "status": Flight.Status.SCHEDULED,
                },
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
                if i % 2 == 1:  # кожне друге місце заброньоване
                    ticket.status = "booked"
                    ticket.save()
                    order, _ = Order.objects.get_or_create(
                        user=user,
                        defaults={
                            "status": "confirmed",
                            "amount": ticket.price,
                            "currency": "USD"
                        }
                    )
                    order.tickets.add(ticket)
                    order.save()

            self.stdout.write(self.style.SUCCESS(f"🎫 Tickets + Orders for {flight.number} created"))