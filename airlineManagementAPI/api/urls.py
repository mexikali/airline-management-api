from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.airplane_views import AirplaneViewSet
from .views.flight_views import FlightViewSet
from .views.reservation_views import ReservationViewSet

router = DefaultRouter()
router.register(r'airplanes', AirplaneViewSet, basename='airplane')
router.register(r'flights', FlightViewSet, basename='flight')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
