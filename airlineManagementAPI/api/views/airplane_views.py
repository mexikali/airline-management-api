"""from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def airplane_view(request):
    return Response({"message": "Airplane View"})"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Airplane, Flight
from api.serializers import AirplaneSerializer, FlightSerializer

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
    

    # POST /airplanes/ (Yeni bir uçak ekle)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
    

    # PATCH /airplanes/{id}/ (Bir uçağın belirli bir alanını güncelle)
    def partial_update(self, request, pk=None):
        try:
            airplane = Airplane.objects.get(pk=pk)
        except Airplane.DoesNotExist:
            return Response({"error": "Airplane not found"}, 404)
        
        serializer = self.get_serializer(airplane, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)


    # DELETE /airplanes/{id}/ (Belirli bir uçağı sil)
    def destroy(self, request, pk=None):
        try:
            airplane = Airplane.objects.get(pk=pk)
            airplane.delete()
            return Response({"message": "Airplane deleted"}, 204)
        except Airplane.DoesNotExist:
            return Response({"error": "Airplane not found"}, 404)
    

    # GET /airplanes/{id}/flights (Belirli bir uçağa ait uçuşları getir)
    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        try:
            airplane = Airplane.objects.get(pk=pk)
            flights = Flight.objects.filter(airplane=airplane)
            serializer = FlightSerializer(flights, many=True)
            return Response(serializer.data, 200)
        except Airplane.DoesNotExist:
            return Response({"error": "Airplane not found"}, 404)
