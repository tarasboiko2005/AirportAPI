import stripe
import logging
import traceback
from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import Payment
from .serializers import PaymentSerializer, CheckoutSessionSerializer
from orders.models import Order

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

@extend_schema(tags=["Payments"])
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by("-id")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=["Payments"])
class CheckoutSessionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CheckoutSessionSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data.get("order_id")

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': order.currency.lower(),
                    'product_data': {'name': f'Order #{order.id}'},
                    'unit_amount': int(order.amount * 100),  # конвертуємо у центи
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            client_reference_id=request.user.id,
            metadata={"order_id": str(order.id)},
        )

        return Response({'id': session.id, 'url': session.url}, status=status.HTTP_201_CREATED)

@extend_schema(tags=["Payments"])
@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    serializer_class = None

    def post(self, request):
        logger.info("Webhook triggered!")
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            logger.error("Signature verification failed")
            return HttpResponse(status=400)

        try:
            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                user_id = session.get("client_reference_id")
                order_id = session.get("metadata", {}).get("order_id")

                if not user_id or not order_id:
                    logger.warning("Missing client_reference_id or order_id")
                    return HttpResponse(status=200)

                try:
                    user = User.objects.get(id=user_id)
                    order = Order.objects.get(id=order_id, user=user)
                except (User.DoesNotExist, Order.DoesNotExist):
                    logger.warning("User or Order not found")
                    return HttpResponse(status=200)

                if Payment.objects.filter(stripe_payment_intent=session.get("payment_intent")).exists():
                    logger.info("Payment already exists, skipping duplicate")
                    return HttpResponse(status=200)

                Payment.objects.update_or_create(
                    stripe_session_id=session.get("id"),
                    defaults={
                        "user": user,
                        "order": order,
                        "amount": Decimal(session.get("amount_total")) / 100,
                        "currency": session.get("currency"),
                        "status": "paid",
                        "stripe_payment_intent": session.get("payment_intent"),
                    }
                )

                order.status = "completed"
                order.save()
                logger.info("Payment and Order updated successfully")
            else:
                logger.info(f"Ignored event type: {event['type']}")

        except Exception as e:
            logger.error("Webhook processing error", exc_info=True)
            traceback.print_exc()

        return HttpResponse(status=200)