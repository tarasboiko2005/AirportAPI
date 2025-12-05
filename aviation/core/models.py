from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)  # ISO
    def __str__(self): return self.name

class Airport(models.Model):
    name = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=3, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='airports')
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
    class Status(models.TextChoices):
        BOOKED = 'booked', 'Booked'
        CANCELLED = 'cancelled', 'Cancelled'
        USED = 'used', 'Used'
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.BOOKED)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('flight', 'seat_number')
    def __str__(self): return f"Ticket {self.id} for {self.user.username}"