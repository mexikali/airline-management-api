from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Flight, Reservation
from api.serializers import FlightSerializer, ReservationSerializer

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


    # POST /flights/ (Yeni bir uçuş ekle)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
    

    # PATCH /flights/{id}/ (Bir uçuşun belirli bir alanını güncelle)
    def partial_update(self, request, pk=None):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, 404)
        
        serializer = self.get_serializer(flight, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)


    # DELETE /flights/{id}/ (Belirli bir uçuşu sil)
    def destroy(self, request, pk=None):
        try:
            flight = Flight.objects.get(pk=pk)
            flight.delete()
            return Response({"message": "Flight deleted"}, 204)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, 404)
    

    # GET /flights/{id}/reservations (Belirli bir uçuşa ait rezervasyonları getir)
    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        try:
            flight = Flight.objects.get(pk=pk)
            reservations = Reservation.objects.filter(flight=flight)
            serializer = ReservationSerializer(reservations, many=True)
            return Response(serializer.data, 200)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found"}, 404)