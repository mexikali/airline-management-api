"""from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def airplane_view(request):
    return Response({"message": "Airplane View"})"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.models import Airplane
from api.serializers import AirplaneSerializer

class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    # Tüm uçakları listeleme (GET /airplanes/)
    def list(self, request):
        airplanes = self.get_queryset()
        serializer = self.get_serializer(airplanes, many=True)
        return Response(serializer.data, 200)

    # Belirli bir uçağın detaylarını alma (GET /airplanes/{id}/)
    def retrieve(self, request, pk=None):
        try:
            airplane = Airplane.objects.get(pk=pk)
            serializer = self.get_serializer(airplane)
            return Response(serializer.data, 200)
        except Airplane.DoesNotExist:
            return Response({"error": "Airplane not found"}, 404)
