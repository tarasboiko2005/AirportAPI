from django.urls import path, include
from rest_framework.routers import DefaultRouter
import debug_toolbar
from .views import (
    FlightViewSet, AirplaneViewSet,
    CountryListCreateView, CountryDetailView,
    AirportListCreateView, AirportDetailView,
    AirlineListView, AirlineDetailView,
    TicketListView, TicketDetailView,
)

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'airplanes', AirplaneViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('countries-generic/', CountryListCreateView.as_view(), name='countries-generic'),
    path('countries-generic/<int:pk>/', CountryDetailView.as_view(), name='country-generic-detail'),

    path('airports-generic/', AirportListCreateView.as_view(), name='airports-generic'),
    path('airports-generic/<int:pk>/', AirportDetailView.as_view(), name='airport-generic-detail'),

    path('airlines-view/', AirlineListView.as_view(), name='airlines-view'),
    path('airlines-view/<int:pk>/', AirlineDetailView.as_view(), name='airline-view-detail'),

    path('tickets-view/', TicketListView.as_view(), name='tickets-view'),
    path('tickets-view/<int:pk>/', TicketDetailView.as_view(), name='ticket-view-detail'),

    path('__debug__/', include(debug_toolbar.urls)),
]