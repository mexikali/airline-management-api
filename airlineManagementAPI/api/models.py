from django.db import models
from unique_code import generate_unique_code


class Airplane(models.Model):
    tail_number = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    production_year = models.IntegerField()
    status = models.BooleanField()



class Flight(models.Model):
    flight_number = models.CharField(max_length=50)
    departure = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)



class Reservation(models.Model):
    passenger_name = models.CharField(max_length=150)
    passenger_email = models.CharField(max_length=150)
    reservation_code = models.CharField(max_length=11, unique=True, blank=True)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            self.reservation_code = generate_unique_code()
            while Reservation.objects.filter(reservation_code=self.reservation_code).exists():
                self.reservation_code = generate_unique_code()
        super().save(*args, **kwargs)
