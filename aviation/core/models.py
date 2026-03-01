from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)  # ISO
    def __str__(self): return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=3, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='airports')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self): return f"{self.name} ({self.iata_code})"

class Airline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='airlines')
    def __str__(self): return self.name

class Airplane(models.Model):
    registration = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=100)
    seats_count = models.PositiveIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    def __str__(self): return f"{self.model} ({self.registration})"

class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        BOARDING = 'boarding', 'Boarding'
        DEPARTED = 'departed', 'Departed'
        DELAYED = 'delayed', 'Delayed'
        CANCELLED = 'cancelled', 'Cancelled'
    number = models.CharField(max_length=10, unique=True)
    origin = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT, related_name='flights')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)
    def __str__(self): return f"Flight {self.number}"

class Ticket(models.Model):
    flight = models.ForeignKey("core.Flight", on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="available")
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets"
    )

    class Meta:
        unique_together = ('flight', 'seat_number')

    def __str__(self):
        return f"Ticket {self.seat_number} for {self.flight.number}"