from typing import Dict, Any, List
from django.db.models import Q

def execute(action: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    from core.models import Flight, Ticket, Airport

    if action == "search_flights":
        filters = params.get("filters", {}) or {}
        origin = filters.get("origin")
        destination = filters.get("destination")
        date = filters.get("date")

        qs = Flight.objects.select_related(
            "origin", "destination", "airplane__airline"
        )

        if origin:
            qs = qs.filter(
                Q(origin__iata_code__iexact=origin) |
                Q(origin__name__icontains=origin)
            )

        if destination:
            qs = qs.filter(
                Q(destination__iata_code__iexact=destination) |
                Q(destination__name__icontains=destination)
            )

        if date:
            from datetime import datetime
            from django.utils.timezone import make_aware
            try:
                d = datetime.fromisoformat(date)
                start = make_aware(d.replace(hour=0, minute=0, second=0, microsecond=0))
                end = make_aware(d.replace(hour=23, minute=59, second=59, microsecond=999999))
                qs = qs.filter(departure_time__range=(start, end))
            except Exception:
                pass

        sort = params.get("sort", {}) or {}
        if sort.get("by"):
            by = sort["by"]
            order = sort.get("order", "asc")
            qs = qs.order_by(by if order == "asc" else f"-{by}")

        limit = params.get("limit", 20)
        return list(qs[:limit].values())

    elif action == "search_countries_from_origin":
        origin = params.get("filters", {}).get("origin")
        date_str = params.get("filters", {}).get("date")

        qs = Flight.objects.all()
        if origin:
            qs = qs.filter(
                Q(origin__iata_code__iexact=origin) |
                Q(origin__name__icontains=origin)
            )

        if date_str:
            from datetime import datetime
            try:
                d = datetime.fromisoformat(date_str).date()
                qs = qs.filter(departure_time__date=d)
            except Exception:
                pass

        countries = qs.values(
            "destination__country__id",
            "destination__country__name",
            "destination__country__code"
        ).distinct()

        return list(countries)

    elif action == "search_airlines_from_airport":
        origin = params.get("filters", {}).get("origin")

        qs = Airport.objects.all()
        if origin:
            qs = qs.filter(
                Q(iata_code__iexact=origin) |
                Q(name__icontains=origin)
            )

        airlines = []
        for airport in qs:
            for airline in airport.airlines.all():
                airlines.append({
                    "name": airline.name,
                    "code": airline.code
                })

        return airlines

    elif action == "search_tickets":
        filters = params.get("filters", {})
        flight_id = filters.get("flight_id")
        qs = Ticket.objects.all()
        if flight_id:
            qs = qs.filter(flight_id=flight_id)
        return list(qs.values())

    elif action == "search_available_tickets":
        filters = params.get("filters", {})
        flight_id = filters.get("flight_id")
        qs = Ticket.objects.filter(status__iexact="available")
        if flight_id:
            qs = qs.filter(flight_id=flight_id)
        return list(qs.values())

    elif action == "search_booked_tickets":
        filters = params.get("filters", {})
        flight_id = filters.get("flight_id")
        qs = Ticket.objects.filter(status__iexact="booked")
        if flight_id:
            qs = qs.filter(flight_id=flight_id)
        return list(qs.values())

    return []