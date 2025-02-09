from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from api.models import Flight, Reservation
from api.serializers import FlightSerializer, ReservationSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    # Tüm uçuşları listeleme (GET /flights/)
    def list(self, request):
        # Query parametrelerini al
        departure_location = request.query_params.get('departure_location', None)
        destination_location = request.query_params.get('destination_location', None)
        departure_date = request.query_params.get('departure_date', None)
        arrival_date = request.query_params.get('arrival_date', None)
        
        # Tüm uçuşları al
        flights = self.get_queryset()
        
        # Q nesnesi ile dinamik filtreleme
        filters = Q()
        
        if departure_location:
            filters &= Q(departure__iexact=departure_location)
        if destination_location:
            filters &= Q(destination__iexact=destination_location)
        
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, "%d-%m-%Y")
                filters &= Q(departure_time__date=departure_date)
            except ValueError:
                return Response({"error": "Invalid departure_date format. Use DD-MM-YYYY."}, 
                                400)

        if arrival_date:
            try:
                arrival_date = datetime.strptime(arrival_date, "%d-%m-%Y")
                filters &= Q(arrival_time__date=arrival_date)
            except ValueError:
                return Response({"error": "Invalid arrival_date format. Use DD-MM-YYYY."}, 
                                400)

        # Filtreleri uygula
        flights = flights.filter(filters)
        
        # Serializer ile veriyi hazırla
        serializer = self.get_serializer(flights, many=True)
        
        # Response döndür
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