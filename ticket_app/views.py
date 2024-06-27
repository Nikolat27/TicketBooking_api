from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from ticket_app import serializers
from ticket_app.models import Ticket


# Create your views here.

class TicketsView(APIView, PageNumberPagination):
    page_size = 1

    def get(self, request):
        tickets = Ticket.objects.all().order_by("-id").distinct()
        paginated_queryset = self.paginate_queryset(tickets, request=request)
        serializer = serializers.TicketSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


# Create
class TicketCreateView(APIView):
    def post(self, request):
        serializer = serializers.TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"response": "You have created your Ticket successfully", "status": status.HTTP_200_OK})


# Read
class TicketDetailView(APIView):
    def get(self, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        serializer = serializers.TicketSerializer(ticket, many=False)
        return Response({"data": serializer.data, "status": status.HTTP_200_OK})


# Update
class TicketUpdateView(APIView):
    def put(self, pk, request):
        ticket = get_object_or_404(Ticket, id=pk)
        serializer = serializers.TicketSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=ticket, validated_data=serializer.validated_data)
        return Response({"response": "You have updated your Ticket successfully",
                         "status": status.HTTP_200_OK})


# Delete
class TicketDeleteView(APIView):
    def delete(self, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        ticket.delete()
        return Response({"response": "You have deleted your ticket successfully",
                         "status": status.HTTP_200_OK})


class TicketFilteringView(APIView):
    def get(self, request):
        flying_from = request.GET.get("flying_from")
        flying_to = request.GET.get("flying_to")
        departing = request.GET.get("departing")  # Format: year-month-day
        trip_type = request.GET.get("trip_type")  # oneway, round
        trip_class = request.GET.get("trip_class")

        passengers = request.GET.get("passengers")
        passengers_list = passengers.split(",")
        passengers_dict = {}

        for passenger in passengers_list:
            key, value = passenger.split(":")
            key = key.strip()
            value = [int(v) for v in value.split()]
            passengers_dict[key] = value

        total_passengers = sum(len(passenger) for passenger in passengers_dict.values())

        # ticket = Ticket.objects.filter(departing_date_date=departing, arrival=flying_from, departure=flying_to,
        #                                ticket_type=trip_type, cabin_class=trip_class)
        ticket = Ticket.objects.get(departing_date__date='2024-06-23')
        print(ticket.free_seats())
        return Response(passengers_dict)
