from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Reservation, Flight
from api.serializers import ReservationSerializer
from api.utils import get_remaining_seats
from airlineManagementAPI.views import send_email
from django.template.loader import render_to_string


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
        
        flight_id = request.data.get("flight")  # Gelen JSON'dan uçuş ID'sini al
        
        if not flight_id:
            return Response({"error": "Flight ID is required."}, 400)
        
        capacity = get_remaining_seats(flight_id=flight_id)
        
        if capacity == -1:
            return Response({"error": "Flight not found."}, 404)
        elif capacity == 0:
            return Response({"error": "No available seats for this flight."}, 400)

        # Kapasite uygunsa rezervasyonu kaydet
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()

            # Flight ve Reservation nesnelerinden gerekli verileri al
            flight = reservation.flight
            
            # HTML içeriğini render et
            html_content = render_to_string(
                'email/confirmation_email.html',  # Şablon yolu
                {
                    'passenger_name': request.data.get('passenger_name'),
                    'reservation_code': reservation.reservation_code,
                    'flight_number': flight.flight_number,
                    'departure_location': flight.departure,
                    'departure_time': flight.departure_time.strftime('%d-%m-%Y %H:%M'),
                    'destination_location': flight.destination,
                    'destination_time': flight.arrival_time.strftime('%d-%m-%Y %H:%M'),
                }
            )
            send_email("Reservation Confirmation", html_content, [request.data.get("passenger_email")])
            return Response(serializer.data, 201)

        return Response(serializer.errors, 400)
    

    # PATCH /reservations/{id}/ (Bir rezervasyonun belirli bir alanını güncelle)
    def partial_update(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, 404)
        
        if "flight" in request.data:
            capacity = get_remaining_seats(flight_id=request.data.get("flight"))
            if capacity == -1:
                return Response({"error": "Flight not found."}, 404)
            elif capacity == 0:
                return Response({"error": "No available seats for this flight."}, 400)

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