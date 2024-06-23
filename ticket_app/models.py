from django.db import models


# Create your models here.


class Airline(models.Model):
    title = models.CharField(max_length=50)
    airlines_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.airlines_code}"


stops = (("Direct", "direct"), ("1 stop", "1 stop"), ("2 stop", "2 stop"))
classes = (("economy", "economy"), ("premium_economy", "premium_economy"), ("business", "business"),
           ("first_class", "first_class"))


class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="A unique identifier for each ticket")
    flight_from = models.CharField(max_length=60)
    flight_from_date = models.DateTimeField()
    flight_to = models.CharField(max_length=60)
    flight_to_date = models.DateTimeField()
    total_passengers = models.PositiveBigIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="airlines")
    price = models.FloatField()
    stops = models.CharField(choices=stops, max_length=10)
    cabin_class = models.CharField(choices=classes, max_length=20)
