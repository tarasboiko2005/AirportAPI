"""
Seed the database with realistic aviation data.
Usage: python manage.py seed_data
"""
import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Country, Airport, Airline, Airplane, Flight, Ticket


class Command(BaseCommand):
    help = "Seed the database with airports, flights, tickets, etc."

    def handle(self, *args, **options):
        self.stdout.write("🌍 Seeding countries...")
        countries = self._seed_countries()

        self.stdout.write("🏢 Seeding airports...")
        airports = self._seed_airports(countries)

        self.stdout.write("✈️ Seeding airlines...")
        airlines = self._seed_airlines(airports)

        self.stdout.write("🛩️ Seeding airplanes...")
        airplanes = self._seed_airplanes(airlines)

        self.stdout.write("🛫 Seeding flights...")
        flights = self._seed_flights(airports, airplanes)

        self.stdout.write("🎫 Seeding tickets...")
        self._seed_tickets(flights)

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))

    def _seed_countries(self):
        data = [
            ("United States", "USA"),
            ("United Kingdom", "GBR"),
            ("Germany", "DEU"),
            ("France", "FRA"),
            ("Japan", "JPN"),
            ("Ukraine", "UKR"),
            ("Turkey", "TUR"),
            ("United Arab Emirates", "ARE"),
            ("Italy", "ITA"),
            ("Spain", "ESP"),
            ("Netherlands", "NLD"),
            ("Canada", "CAN"),
            ("Australia", "AUS"),
            ("South Korea", "KOR"),
            ("Poland", "POL"),
            ("Switzerland", "CHE"),
        ]
        result = {}
        for name, code in data:
            obj, created = Country.objects.get_or_create(code=code, defaults={"name": name})
            result[code] = obj
            if created:
                self.stdout.write(f"  + {name}")
        return result

    def _seed_airports(self, countries):
        data = [
            ("John F. Kennedy International", "JFK", "USA", 40.6413, -73.7781),
            ("Los Angeles International", "LAX", "USA", 33.9416, -118.4085),
            ("Chicago O'Hare International", "ORD", "USA", 41.9742, -87.9073),
            ("San Francisco International", "SFO", "USA", 37.6213, -122.3790),
            ("Miami International", "MIA", "USA", 25.7959, -80.2870),
            ("Heathrow Airport", "LHR", "GBR", 51.4700, -0.4543),
            ("Gatwick Airport", "LGW", "GBR", 51.1537, -0.1821),
            ("Frankfurt Airport", "FRA", "DEU", 50.0379, 8.5622),
            ("Munich Airport", "MUC", "DEU", 48.3537, 11.7750),
            ("Charles de Gaulle Airport", "CDG", "FRA", 49.0097, 2.5479),
            ("Narita International", "NRT", "JPN", 35.7720, 140.3929),
            ("Haneda Airport", "HND", "JPN", 35.5494, 139.7798),
            ("Boryspil International", "KBP", "UKR", 50.3450, 30.8947),
            ("Lviv Danylo Halytskyi", "LWO", "UKR", 49.8125, 23.9561),
            ("Istanbul Airport", "IST", "TUR", 41.2608, 28.7418),
            ("Dubai International", "DXB", "ARE", 25.2532, 55.3657),
            ("Rome Fiumicino", "FCO", "ITA", 41.8003, 12.2389),
            ("Barcelona El Prat", "BCN", "ESP", 41.2974, 2.0833),
            ("Madrid Barajas", "MAD", "ESP", 40.4983, -3.5676),
            ("Amsterdam Schiphol", "AMS", "NLD", 52.3105, 4.7683),
            ("Toronto Pearson", "YYZ", "CAN", 43.6777, -79.6248),
            ("Sydney Kingsford Smith", "SYD", "AUS", -33.9461, 151.1772),
            ("Incheon International", "ICN", "KOR", 37.4602, 126.4407),
            ("Warsaw Chopin", "WAW", "POL", 52.1657, 20.9671),
            ("Zurich Airport", "ZRH", "CHE", 47.4647, 8.5492),
        ]
        result = {}
        for name, iata, country_code, lat, lng in data:
            obj, created = Airport.objects.get_or_create(
                iata_code=iata,
                defaults={
                    "name": name,
                    "country": countries[country_code],
                    "latitude": lat,
                    "longitude": lng,
                },
            )
            if not created and (obj.latitude is None):
                obj.latitude = lat
                obj.longitude = lng
                obj.save()
            result[iata] = obj
            if created:
                self.stdout.write(f"  + {name} ({iata})")
        return result

    def _seed_airlines(self, airports):
        data = [
            ("American Airlines", "AA", "JFK"),
            ("British Airways", "BA", "LHR"),
            ("Lufthansa", "LH", "FRA"),
            ("Air France", "AF", "CDG"),
            ("United Airlines", "UA", "ORD"),
            ("Turkish Airlines", "TK", "IST"),
            ("Emirates", "EK", "DXB"),
            ("Japan Airlines", "JL", "NRT"),
            ("KLM Royal Dutch", "KL", "AMS"),
            ("Ukraine International", "PS", "KBP"),
            ("Qantas", "QF", "SYD"),
            ("Swiss International", "LX", "ZRH"),
        ]
        result = {}
        for name, code, hub_iata in data:
            obj, created = Airline.objects.get_or_create(
                code=code,
                defaults={"name": name, "airport": airports[hub_iata]},
            )
            result[code] = obj
            if created:
                self.stdout.write(f"  + {name}")
        return result

    def _seed_airplanes(self, airlines):
        models_pool = [
            ("Boeing 737-800", 189),
            ("Boeing 777-300ER", 396),
            ("Boeing 787-9 Dreamliner", 290),
            ("Airbus A320neo", 180),
            ("Airbus A330-300", 277),
            ("Airbus A350-900", 325),
            ("Airbus A380-800", 555),
            ("Embraer E190", 100),
        ]
        airline_codes = list(airlines.keys())
        result = []
        reg_counter = 100
        for i in range(18):
            model_name, seats = random.choice(models_pool)
            airline = airlines[airline_codes[i % len(airline_codes)]]
            reg = f"N{reg_counter + i}AP"
            obj, created = Airplane.objects.get_or_create(
                registration=reg,
                defaults={
                    "model": model_name,
                    "seats_count": seats,
                    "airline": airline,
                },
            )
            result.append(obj)
            if created:
                self.stdout.write(f"  + {model_name} ({reg})")
        return result

    def _seed_flights(self, airports, airplanes):
        routes = [
            ("JFK", "LHR"), ("LHR", "JFK"),
            ("JFK", "CDG"), ("CDG", "JFK"),
            ("LAX", "NRT"), ("NRT", "LAX"),
            ("ORD", "FRA"), ("FRA", "ORD"),
            ("JFK", "DXB"), ("DXB", "JFK"),
            ("LHR", "IST"), ("IST", "LHR"),
            ("CDG", "FCO"), ("FCO", "CDG"),
            ("KBP", "WAW"), ("WAW", "KBP"),
            ("KBP", "IST"), ("IST", "KBP"),
            ("AMS", "BCN"), ("BCN", "AMS"),
            ("SFO", "ICN"), ("ICN", "SFO"),
            ("MIA", "MAD"), ("MAD", "MIA"),
            ("LHR", "DXB"), ("DXB", "LHR"),
            ("YYZ", "LHR"), ("LHR", "YYZ"),
            ("SYD", "LAX"), ("LAX", "SYD"),
            ("FRA", "NRT"), ("NRT", "FRA"),
            ("ZRH", "JFK"), ("JFK", "ZRH"),
            ("MUC", "KBP"), ("KBP", "MUC"),
            ("LWO", "WAW"), ("WAW", "LWO"),
        ]

        statuses = [
            Flight.Status.SCHEDULED,
            Flight.Status.SCHEDULED,
            Flight.Status.SCHEDULED,
            Flight.Status.SCHEDULED,
            Flight.Status.BOARDING,
            Flight.Status.DELAYED,
        ]

        now = timezone.now()
        result = []
        flight_num = 100

        for i, (orig_iata, dest_iata) in enumerate(routes):
            number = f"SK{flight_num + i}"
            if Flight.objects.filter(number=number).exists():
                result.append(Flight.objects.get(number=number))
                continue

            dep_offset_hours = random.randint(2, 720)  # 2h to 30 days ahead
            dep_time = now + timedelta(hours=dep_offset_hours)
            flight_duration = timedelta(hours=random.randint(1, 14), minutes=random.choice([0, 15, 30, 45]))
            arr_time = dep_time + flight_duration

            flight = Flight.objects.create(
                number=number,
                origin=airports[orig_iata],
                destination=airports[dest_iata],
                departure_time=dep_time,
                arrival_time=arr_time,
                airplane=random.choice(airplanes),
                status=random.choice(statuses),
            )
            result.append(flight)
            self.stdout.write(f"  + {number}: {orig_iata} → {dest_iata}")

        return result

    def _seed_tickets(self, flights):
        rows = list(range(1, 31))
        cols = ["A", "B", "C", "D", "E", "F"]
        created_count = 0

        for flight in flights:
            existing = Ticket.objects.filter(flight=flight).count()
            if existing > 0:
                continue

            num_tickets = random.randint(6, 12)
            seats_used = set()

            for _ in range(num_tickets):
                while True:
                    seat = f"{random.choice(rows)}{random.choice(cols)}"
                    if seat not in seats_used:
                        seats_used.add(seat)
                        break

                price = Decimal(str(random.randint(50, 800))) + Decimal("0.99")
                is_booked = random.random() < 0.3
                status = "booked" if is_booked else "available"

                Ticket.objects.create(
                    flight=flight,
                    seat_number=seat,
                    price=price,
                    status=status,
                )
                created_count += 1

        self.stdout.write(f"  Created {created_count} tickets total")
