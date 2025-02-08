"""from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def reservation_view(request):
    return Response({"message": "Reservation View"})"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.models import Reservation
from api.serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    # Tüm rezervasyonları listeleme (GET /reservations/)
    def list(self, request):
        reservations = self.get_queryset()
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data, 200)

    # Belirli bir rezervasyonun detaylarını alma (GET /reservations/{id}/)
    def retrieve(self, request, pk=None):
        try:
            reservations = Reservation.objects.get(pk=pk)
            serializer = self.get_serializer(reservations)
            return Response(serializer.data, 200)
        except Reservation.DoesNotExist:
            return Response({"error": "Flight not found"}, 404)
    

    # POST /reservations/ (Yeni bir rezervasyon ekle)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
    

    # PATCH /reservations/{id}/ (Bir rezervasyonun belirli bir alanını güncelle)
    def partial_update(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, 404)
        
        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)


    # DELETE /reservations/{id}/ (Belirli bir rezervasyonu sil)
    def destroy(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.delete()
            return Response({"message": "Reservation deleted"}, 204)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, 404)