from django.db import models


# Create your models here.


class Airline(models.Model):
    title = models.CharField(max_length=50)
    airlines_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.airlines_code}"


stops = (("direct", "Direct"), ("1 stop", "1 stop"), ("2 stop", "2 Stops"))
classes = (("economy", "Economy"), ("premium_economy", "Premium Economy"), ("business", "Business"),
           ("first_class", "First Class"))
ticket_types = (
    ('one_way', "One Way"),
    ("round_trip", "Round Trip")
)


class Ticket(models.Model):
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="A unique identifier for each ticket")
    departure = models.CharField(max_length=60)
    departing_date = models.DateTimeField()
    arrival = models.CharField(max_length=60)
    arriving_date = models.DateTimeField()
    total_passengers = models.PositiveBigIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name="airlines")
    airplane = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField()
    stops = models.CharField(choices=stops, max_length=10)
    allowed_weight = models.FloatField(verbose_name="Must be in Kilogram", default=20)
    booked_up = models.BooleanField(default=False, verbose_name="Means that all the tickets have been booked")
    ticket_type = models.CharField(choices=ticket_types, max_length=20, default=ticket_types[0])
    cabin_class = models.CharField(choices=classes, max_length=20)
    return_date = models.DateTimeField(blank=True, null=True, verbose_name="Just use this field if you have chosen"
                                                                           " 'Round Trip'")

    def __str__(self):
        return f"{self.ticket_type} - {self.departure} - {self.arrival}"

    def flight_duration(self): # How long does it take to reach to the destination
        return self.departing_date - self.arriving_date
