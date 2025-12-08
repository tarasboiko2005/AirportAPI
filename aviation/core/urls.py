from django.urls import path, include
from rest_framework.routers import DefaultRouter
import debug_toolbar
from .views import (
    # ViewSets
    UserViewSet, FlightViewSet, AirplaneViewSet,

    # Generic Views (розділені)
    CountryListCreateView, CountryDetailView,
    AirportListCreateView, AirportDetailView,

    # APIViews
    AirlineListView, AirlineDetailView,
    TicketListView, TicketDetailView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'airplanes', AirplaneViewSet)

urlpatterns = [
    # ViewSets через router
    path('', include(router.urls)),

    # Countries через GenericAPIView
    path('countries-generic/', CountryListCreateView.as_view(), name='countries-generic'),
    path('countries-generic/<int:pk>/', CountryDetailView.as_view(), name='country-generic-detail'),

    # Airports через GenericAPIView
    path('airports-generic/', AirportListCreateView.as_view(), name='airports-generic'),
    path('airports-generic/<int:pk>/', AirportDetailView.as_view(), name='airport-generic-detail'),

    # Airlines через APIView
    path('airlines-view/', AirlineListView.as_view(), name='airlines-view'),
    path('airlines-view/<int:pk>/', AirlineDetailView.as_view(), name='airline-view-detail'),

    # Tickets через APIView
    path('tickets-view/', TicketListView.as_view(), name='tickets-view'),
    path('tickets-view/<int:pk>/', TicketDetailView.as_view(), name='ticket-view-detail'),

    # Debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),
]