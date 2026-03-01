import json
import logging
import urllib.request
import urllib.parse
import urllib.error

from django.utils import timezone
from django.db.models import Min, Max, Q
from core.models import Flight, Ticket, Airport, Airline
from orders.models import Order

logger = logging.getLogger("assistant")


def search_flights(
    destination: str,
    departure_city: str = None,
    date_from: str = None,
    date_to: str = None,
):
    """Search for scheduled flights by destination, optional origin city, and date range."""

    flights = Flight.objects.filter(
        Q(destination__name__icontains=destination)
        | Q(destination__iata_code__iexact=destination),
        status=Flight.Status.SCHEDULED,
    )

    if departure_city:
        flights = flights.filter(
            Q(origin__name__icontains=departure_city)
            | Q(origin__iata_code__iexact=departure_city)
        )

    if date_from and date_to:
        flights = flights.filter(
            departure_time__date__range=[date_from, date_to]
        )
    elif date_from:
        flights = flights.filter(departure_time__date=date_from)
    else:
        today = timezone.now().date()
        flights = flights.filter(departure_time__date__gte=today)

    flights = flights.select_related(
        "origin", "destination", "airplane", "airplane__airline"
    ).order_by("departure_time")[:10]

    data = [
        {
            "id": f.id,
            "number": f.number,
            "route": f"{f.origin.name} ({f.origin.iata_code}) -> {f.destination.name} ({f.destination.iata_code})",
            "departure_time": f.departure_time.strftime("%Y-%m-%d %H:%M"),
            "arrival_time": f.arrival_time.strftime("%Y-%m-%d %H:%M"),
            "airline": f.airplane.airline.name if f.airplane and f.airplane.airline else "N/A",
            "airplane": f"{f.airplane.model} ({f.airplane.registration})" if f.airplane else "N/A",
            "status": f.status,
        }
        for f in flights
    ]

    if not data:
        return "No flights found for the given criteria."

    return json.dumps(data, ensure_ascii=False)


def get_user_orders(email: str):
    """Get recent orders for a user by their email address."""

    orders = Order.objects.filter(user__email__iexact=email).order_by(
        "-created_at"
    )[:5]

    if not orders.exists():
        return "No orders found for this user."

    data = []
    for o in orders:
        tickets_info = [
            {
                "flight": f"{t.flight.origin.name} -> {t.flight.destination.name}",
                "flight_number": t.flight.number,
                "date": t.flight.departure_time.strftime("%Y-%m-%d %H:%M"),
                "seat": t.seat_number,
                "status": t.status,
                "price": str(t.price),
            }
            for t in o.tickets.select_related(
                "flight", "flight__origin", "flight__destination"
            )
        ]

        data.append(
            {
                "order_id": o.id,
                "status": o.status,
                "total_price": str(o.amount),
                "currency": o.currency,
                "created_at": o.created_at.strftime("%Y-%m-%d %H:%M"),
                "tickets": tickets_info,
            }
        )

    return json.dumps(data, ensure_ascii=False)


def get_ticket_details(flight_id: int):
    """Get available ticket details (seats, prices) for a specific flight by its ID."""

    try:
        flight = Flight.objects.select_related(
            "origin", "destination"
        ).get(id=flight_id)
    except Flight.DoesNotExist:
        return "Flight not found with that ID."

    available = Ticket.objects.filter(flight=flight, status="available")
    total_free = available.count()

    if total_free == 0:
        return f"No available seats for flight {flight.number} ({flight.origin.name} -> {flight.destination.name})."

    min_price = available.aggregate(Min("price"))["price__min"]
    max_price = available.aggregate(max_p=Max("price"))["max_p"] if total_free > 1 else min_price

    seats_list = list(
        available.values_list("seat_number", flat=True).order_by("seat_number")[:20]
    )

    response = {
        "flight_id": flight.id,
        "flight_number": flight.number,
        "route": f"{flight.origin.name} ({flight.origin.iata_code}) -> {flight.destination.name} ({flight.destination.iata_code})",
        "available_seats": total_free,
        "min_price": str(min_price) if min_price else "N/A",
        "sample_seats": seats_list,
    }
    return json.dumps(response, ensure_ascii=False)


def search_airports(query: str):
    """Search airports by name, IATA code, or country name."""

    airports = Airport.objects.filter(
        Q(name__icontains=query)
        | Q(iata_code__iexact=query)
        | Q(country__name__icontains=query)
    ).select_related("country")[:10]

    if not airports.exists():
        return "No airports found matching your query."

    data = [
        {
            "id": a.id,
            "name": a.name,
            "iata_code": a.iata_code,
            "country": a.country.name,
        }
        for a in airports
    ]
    return json.dumps(data, ensure_ascii=False)


def search_airlines(query: str):
    """Search airlines by name or airline code."""

    airlines = Airline.objects.filter(
        Q(name__icontains=query) | Q(code__iexact=query)
    ).select_related("airport", "airport__country")[:10]

    if not airlines.exists():
        return "No airlines found matching your query."

    data = [
        {
            "id": a.id,
            "name": a.name,
            "code": a.code,
            "base_airport": f"{a.airport.name} ({a.airport.iata_code})",
            "country": a.airport.country.name,
        }
        for a in airlines
    ]
    return json.dumps(data, ensure_ascii=False)


def get_weather(city: str):
    """Get current weather for a city or country to help travelers plan trips."""

    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "AirportAPI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            weather_data = json.loads(resp.read().decode("utf-8"))

        current = weather_data.get("current_condition", [{}])[0]
        area = weather_data.get("nearest_area", [{}])[0]

        area_name = area.get("areaName", [{}])[0].get("value", city)
        country = area.get("country", [{}])[0].get("value", "")

        result = {
            "location": f"{area_name}, {country}" if country else area_name,
            "temperature_c": current.get("temp_C", "N/A"),
            "feels_like_c": current.get("FeelsLikeC", "N/A"),
            "description": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
            "humidity": f"{current.get('humidity', 'N/A')}%",
            "wind_speed_kmh": current.get("windspeedKmph", "N/A"),
            "wind_direction": current.get("winddir16Point", "N/A"),
            "visibility_km": current.get("visibility", "N/A"),
        }
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        logger.warning(f"Weather API error for '{city}': {e}")
        return f"Could not fetch weather data for '{city}'. The weather service may be temporarily unavailable."