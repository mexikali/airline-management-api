from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.airplane_views import *
from .views.flight_views import *
from .views.reservation_views import *

"""urlpatterns = [
    path('airplane/', airplane_view),
    path('flight/', flight_view),
    path('reservation/', reservation_view),
]"""

router = DefaultRouter()
router.register(r'airplanes', AirplaneViewSet, basename='airplane')
router.register(r'flights', AirplaneViewSet, basename='flight')
router.register(r'reservations', AirplaneViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),  # Tüm DRF endpointlerini otomatik ekler
]