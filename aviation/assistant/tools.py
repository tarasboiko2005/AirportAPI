import json
from django.utils import timezone
from django.db.models import Min, Q
from core.models import Flight, Ticket
from orders.models import Order

def search_flights(destination: str, departure_city: str = None,
                   date_from: str = None, date_to: str = None):

    flights = Flight.objects.filter(
        Q(destination__name__icontains=destination) |
        Q(destination__iata_code__iexact=destination),
        status=Flight.Status.SCHEDULED
    )

    if departure_city:
        flights = flights.filter(
            Q(origin__name__icontains=departure_city) |
            Q(origin__iata_code__iexact=departure_city)
        )

    if date_from and date_to:
        flights = flights.filter(departure_time__date__range=[date_from, date_to])
    elif date_from:
        flights = flights.filter(departure_time__date=date_from)
    else:
        today = timezone.now().date()
        flights = flights.filter(departure_time__date__gte=today)

    flights = flights.order_by("departure_time")[:5]

    data = [{
        "id": f.id,
        "route": f"{f.origin.name} -> {f.destination.name}",
        "departure_time": f.departure_time.strftime("%Y-%m-%d %H:%M"),
        "arrival_time": f.arrival_time.strftime("%Y-%m-%d %H:%M"),
        "status": f.status,
    } for f in flights]

    if not data:
        return "No flights found."

    return json.dumps(data)


def get_user_orders(email: str):
    orders = Order.objects.filter(user__email__iexact=email).order_by("-created_at")[:5]

    if not orders.exists():
        return "No orders found."

    data = []
    for o in orders:
        tickets_info = [{
            "flight": f"{t.flight.origin.name} -> {t.flight.destination.name}",
            "date": t.flight.departure_time.strftime("%Y-%m-%d"),
            "seat": t.seat_number,
            "status": t.status,
            "price": str(t.price)
        } for t in o.tickets.all()]

        data.append({
            "order_id": o.id,
            "status": o.status,
            "total_price": str(o.amount),
            "tickets": tickets_info
        })

    return json.dumps(data)


def get_ticket_details(flight_id: int):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return "Flight ID not found."

    available = Ticket.objects.filter(flight=flight, status="available")
    total_free = available.count()
    if total_free == 0:
        return "No seats available."

    prices = {}
    min_price = available.aggregate(Min("price"))["price__min"]
    if min_price:
        prices["min_price"] = str(min_price)

    response = {
        "flight_id": flight.id,
        "available_seats": total_free,
        "prices": prices
    }
    return json.dumps(response)


def map_intent(intent: dict):
    raw_action = intent.get("action") or intent.get("intent") or intent.get("command") or "unknown"
    params = intent.get("params") or intent.get("parameters") or {}

    normalized = str(raw_action).strip().lower().replace("_", " ").replace("-", " ")

    action_map = {
        "search flights": "search_flights",
        "find flights": "search_flights",
        "get ticket details": "get_ticket_details",
        "tickets": "get_ticket_details",
        "get user orders": "get_user_orders",
        "refusal": "refusal",
    }

    action = action_map.get(normalized, "unknown")
    return action, params


SUGGESTIONS = {
    "Flights": "Would you like to check available tickets for this flight?",
    "Tickets": "Would you like to place an order for this ticket?",
    "Orders": "Would you like to check the payment status of these orders?"
}

def wrap_response(entity: str, data):
    suggestion = SUGGESTIONS.get(entity)

    if not data or (isinstance(data, list) and len(data) == 0):
        response = {
            "action": "refusal",
            "params": {"message": f"{entity} not found."}
        }
        if suggestion:
            response["suggestion"] = suggestion
        return response

    response = {
        "status": "success",
        "message": "Success",
        "data": data
    }
    if suggestion:
        response["suggestion"] = suggestion
    return response