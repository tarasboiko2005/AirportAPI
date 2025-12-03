from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import debug_toolbar
from .views import (
    UserViewSet, CountryViewSet, AirportViewSet,
    AirlineViewSet, AirplaneViewSet, FlightViewSet, TicketViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('__debug__/', include(debug_toolbar.urls)),
]