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

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Test Ticket'},
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            client_reference_id=request.user.id,
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

                if not user_id:
                    logger.warning("No client_reference_id in session")
                    return HttpResponse(status=200)

                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    logger.warning(f"User with id {user_id} not found")
                    return HttpResponse(status=200)

                if Payment.objects.filter(stripe_payment_intent=session.get("payment_intent")).exists():
                    logger.info("Payment already exists, skipping duplicate")
                    return HttpResponse(status=200)

                stripe_session_id = session.get("id")
                amount = session.get("amount_total")
                currency = session.get("currency")

                Payment.objects.update_or_create(
                    stripe_session_id=stripe_session_id,
                    defaults={
                        "user": user,
                        "amount": Decimal(amount) / 100,
                        "currency": currency,
                        "status": "completed",
                    }
                )

                logger.info("Payment created successfully")
            else:
                logger.info(f"Ignored event type: {event['type']}")

        except Exception as e:
            logger.error("Webhook processing error", exc_info=True)
            traceback.print_exc()

        return HttpResponse(status=200)