from rest_framework import serializers
from .models import Order
from core.models import Ticket

class OrderSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.filter(status='available'),
        many=True,
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'amount', 'payment_method', 'status', 'created_at', 'updated_at', 'tickets']
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'amount', 'user']

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