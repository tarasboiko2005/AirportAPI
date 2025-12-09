from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.models import Ticket
from .models import Order
from .serializers import OrderSerializer

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)

        tickets_ids = self.request.data.get("tickets", [])
        for ticket_id in tickets_ids:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = "booked"
            ticket.order = order
            ticket.save()

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)





