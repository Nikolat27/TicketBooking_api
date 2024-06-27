from rest_framework import serializers
from . import models


class TicketSerializer(serializers.ModelSerializer):
    flight_duration = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()
    passengers = serializers.SerializerMethodField()
    free_seats = serializers.SerializerMethodField()

    class Meta:
        model = models.Ticket
        fields = "__all__"

    def get_flight_duration(self, obj):
        return obj.flight_duration()

    def get_time_left(self, obj):
        return obj.time_left()

    def get_passengers(self, obj):
        return obj.passengers()

    def get_free_seats(self, obj):
        return obj.free_seats()
