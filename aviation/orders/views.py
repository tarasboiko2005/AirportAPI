from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Order
from .serializers import OrderSerializer


@extend_schema(
    tags=["Orders"],
    responses=OrderSerializer,
    request=OrderSerializer
)
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.filter(user=self.request.user)
        # Auto-expire booked orders past their expiry time
        now = timezone.now()
        expired_orders = qs.filter(status='booked', expires_at__lt=now)
        for order in expired_orders:
            order.status = 'expired'
            order.save()
            # Release tickets back to available
            order.tickets.update(status='available', order=None)

        # Return only active orders (not expired)
        return qs.exclude(status='expired')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=["Orders"],
    responses=OrderSerializer,
    request=OrderSerializer
)
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)