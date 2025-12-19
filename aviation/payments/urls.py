from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, CheckoutSessionViewSet, StripeWebhookView
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'checkout-session', CheckoutSessionViewSet, basename='checkout-session')

urlpatterns = router.urls + [
    path("success", lambda request: HttpResponse("✅ Payment success!")),
    path("cancel", lambda request: HttpResponse("❌ Payment cancel!")),
    path("webhook/", StripeWebhookView.as_view(), name="stripe-webhook")
]