from .models import Flight, Reservation

def get_remaining_seats(flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return -1  # Uçuş bulunamazsa -1 döndür
    
    total_capacity = flight.airplane.capacity
    reserved_seats = Reservation.objects.filter(flight=flight).count()

    return total_capacity - reserved_seats  # Kalan kapasiteyi döndür
