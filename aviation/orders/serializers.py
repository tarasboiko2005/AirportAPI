from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.utils import timezone

from users.serializers import UserSerializer
from .models import Order
from core.models import Ticket
from core.serializers import TicketSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    tickets = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.filter(status='available'),
        many=True,
        write_only=True
    )

    tickets_info = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'amount', 'currency', 'payment_method', 'status',
            'created_at', 'updated_at', 'expires_at', 'tickets', 'tickets_info',
            'time_remaining'
        ]
        read_only_fields = [
            'id', 'user', 'amount', 'status', 'created_at', 'updated_at', 'expires_at'
        ]

    @extend_schema_field(serializers.ListSerializer(child=TicketSerializer()))
    def get_tickets_info(self, obj) -> list[dict]:
        return TicketSerializer(obj.tickets.all(), many=True).data

    def get_time_remaining(self, obj) -> int | None:
        """Seconds remaining before order expires. None if paid/cancelled."""
        if obj.status in ('paid', 'cancelled', 'expired'):
            return None
        if obj.expires_at:
            delta = (obj.expires_at - timezone.now()).total_seconds()
            return max(0, int(delta))
        return None

    def create(self, validated_data):
        tickets = validated_data.pop('tickets')
        user = self.context['request'].user
        validated_data.pop('user', None)

        amount = sum(ticket.price for ticket in tickets)

        order = Order.objects.create(user=user, amount=amount, **validated_data)

        for ticket in tickets:
            ticket.status = 'booked'
            ticket.order = order
            ticket.save()

        return order