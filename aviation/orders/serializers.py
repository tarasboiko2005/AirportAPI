from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

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

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'amount', 'currency', 'payment_method', 'status',
            'created_at', 'updated_at', 'tickets', 'tickets_info'
        ]
        read_only_fields = [
            'id', 'user', 'amount', 'status', 'created_at', 'updated_at'
        ]

    @extend_schema_field(serializers.ListSerializer(child=TicketSerializer()))
    def get_tickets_info(self, obj) -> list[dict]:
        return TicketSerializer(obj.tickets.all(), many=True).data

    def create(self, validated_data):
        tickets = validated_data.pop('tickets')
        user = self.context['request'].user
        validated_data.pop('user', None)

        amount = sum(ticket.price for ticket in tickets)

        order = Order.objects.create(user=user, amount=amount, **validated_data)

        # оновлюємо статус квитків і прив’язуємо їх до ордера
        for ticket in tickets:
            ticket.status = 'booked'
            ticket.order = order
            ticket.save()

        return order