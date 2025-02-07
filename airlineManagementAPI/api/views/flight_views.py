"""from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def flight_view(request):
    return Response({"message": "Flight View"})"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.models import Flight
from api.serializers import FlightSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    # Tüm uçuşları listeleme (GET /flights/)
    def list(self, request):
        flights = self.get_queryset()
        serializer = self.get_serializer(flights, many=True)
        return Response(serializer.data, 200)

    # Belirli bir uçuşun detaylarını alma (GET /flights/{id}/)
    def retrieve(self, request, pk=None):
        try:
            flights = Flight.objects.get(pk=pk)
            serializer = self.get_serializer(flights)
            return Response(serializer.data, 200)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, 404)
