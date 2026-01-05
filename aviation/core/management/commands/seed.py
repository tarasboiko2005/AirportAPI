from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from core.models import Country, Airport, Airline, Airplane, Flight, Ticket
from orders.models import Order


class Command(BaseCommand):
    help = "Seed test flights Lviv -> Krakow (tomorrow and day after tomorrow) + sample order"

    def handle(self, *args, **options):
        tomorrow = timezone.now() + timedelta(days=1)
        day_after_tomorrow = timezone.now() + timedelta(days=2)

        # Countries
        ukraine, _ = Country.objects.update_or_create(
            code="UA",
            defaults={"name": "Ukraine"}
        )
        poland, _ = Country.objects.update_or_create(
            code="PL",
            defaults={"name": "Poland"}
        )

        # Airports
        lviv_airport, _ = Airport.objects.update_or_create(
            iata_code="LWO",
            defaults={"name": "Lviv", "country": ukraine}
        )
        krakow_airport, _ = Airport.objects.update_or_create(
            iata_code="KRK",
            defaults={"name": "Krakow", "country": poland}
        )

        # Airline + Airplane (для першого рейсу)
        airline, _ = Airline.objects.update_or_create(
            code="TA123",
            defaults={"name": "TestAir", "airport": lviv_airport}
        )
        airplane, _ = Airplane.objects.update_or_create(
            registration="UR-TEST",
            defaults={"model": "Boeing 737", "seats_count": 180, "airline": airline}
        )

        # Flight Lviv -> Krakow (завтра)
        flight, created = Flight.objects.update_or_create(
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
            self.stdout.write(self.style.SUCCESS("✅ Flight Lviv -> Krakow (tomorrow) created"))
        else:
            self.stdout.write(self.style.SUCCESS("🔄 Flight Lviv -> Krakow (tomorrow) updated"))

        # Tickets для першого рейсу
        tickets = []
        for seat in ["1A", "1B", "2A", "2B"]:
            t, _ = Ticket.objects.update_or_create(
                flight=flight,
                seat_number=seat,
                defaults={"price": 120.00, "status": "available"}
            )
            tickets.append(t)
        self.stdout.write(self.style.SUCCESS("🎫 Tickets for Lviv -> Krakow (tomorrow) ensured"))

        # Airline + Airplane (для другого рейсу)
        airline2, _ = Airline.objects.update_or_create(
            code="TA789",
            defaults={"name": "TestAir2", "airport": lviv_airport}
        )
        airplane2, _ = Airplane.objects.update_or_create(
            registration="UR-TEST3",
            defaults={"model": "Embraer 190", "seats_count": 100, "airline": airline2}
        )

        # Flight Lviv -> Krakow (післязавтра)
        flight2, created2 = Flight.objects.update_or_create(
            number="TA3003",
            defaults={
                "origin": lviv_airport,
                "destination": krakow_airport,
                "departure_time": day_after_tomorrow.replace(hour=9, minute=0, second=0, microsecond=0),
                "arrival_time": day_after_tomorrow.replace(hour=10, minute=10, second=0, microsecond=0),
                "airplane": airplane2,
                "status": Flight.Status.SCHEDULED,
            }
        )
        if created2:
            self.stdout.write(self.style.SUCCESS("✅ Flight Lviv -> Krakow (day after tomorrow) created"))
        else:
            self.stdout.write(self.style.SUCCESS("🔄 Flight Lviv -> Krakow (day after tomorrow) updated"))

        # Tickets для другого рейсу
        for seat in ["5A", "5B", "6A", "6B"]:
            Ticket.objects.update_or_create(
                flight=flight2,
                seat_number=seat,
                defaults={"price": 130.00, "status": "available"}
            )
        self.stdout.write(self.style.SUCCESS("🎫 Tickets for Lviv -> Krakow (day after tomorrow) ensured"))

        # --- Order ---
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            email="tarasboiko2005@gmail.com",
            defaults={"username": "taras", "password": "testpass123"}
        )

        order, created_order = Order.objects.get_or_create(
            user=user,
            status="confirmed",
            defaults={"amount": sum(float(t.price) for t in tickets)}
        )
        order.tickets.set(tickets)

        if created_order:
            self.stdout.write(self.style.SUCCESS("🧾 Sample order created for user tarasboiko2005@gmail.com"))
        else:
            self.stdout.write(self.style.SUCCESS("🔄 Sample order updated for user tarasboiko2005@gmail.com"))