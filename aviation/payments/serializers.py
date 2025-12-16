from rest_framework import serializers
from .models import Payment

class CheckoutSessionSerializer(serializers.Serializer):
    id = serializers.CharField()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "order",
            "stripe_session_id",
            "stripe_payment_intent",
            "amount",
            "currency",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "created_at", "updated_at"]

class EmptySerializer(serializers.Serializer):
    pass
