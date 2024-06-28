import jwt
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from TicketBooking_api import settings
from accounts_app.models import User
from ticket_app import serializers
from ticket_app.models import Ticket, TicketBooked


# Create your views here.

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization', None)
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        return (None, None)


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
    def put(self, request, pk):
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


class TicketFilteringView(APIView, PageNumberPagination):
    page_size = 1

    def get(self, request):
        flying_from = request.GET.get("flying_from")
        flying_to = request.GET.get("flying_to")
        departing = request.GET.get("departing")  # Format: year-month-day
        ticket_type = request.GET.get("ticket_type")  # one_way, round_trip
        ticket_class = request.GET.get("ticket_class")
        passengers = request.GET.get("passengers")

        passengers_list = passengers.split(",")
        passengers_dict = {}

        for passenger in passengers_list:
            key, value = passenger.split(",")
            value = value.strip("[").strip("]").split(";")
            value = [int(v) for v in value]
            passengers_dict[key] = value

        passengers_count = sum(len(passenger) for passenger in passengers_dict.values())
        tickets = Ticket.objects.annotate(
            total_booked=Count('tickets_booked__passengers')
        ).filter(total_booked__lte=F('total_passengers') - passengers_count)  # F is model field value

        filter_params = {
            'departure': flying_from,
            'arrival': flying_to,
            'departing_date__date': departing,
            'ticket_type': ticket_type,
            'cabin_class': ticket_class,
        }

        if ticket_type == "round_trip":
            return_date = request.GET.get("return_date")
            if return_date:
                filter_params.update({
                    'return_date__date': return_date
                })

        tickets = tickets.filter(**filter_params).order_by("-id").distinct()
        paginated_queryset = self.paginate_queryset(tickets, request=request)
        serializer = serializers.TicketSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class TicketPurchaseView(APIView):
    def get(self, request, pk):
        print(request.user)
        ticket = get_object_or_404(Ticket, id=pk)
        passengers = 'children:[12;13;15],adults:2,infants:1'
        passengers_list = passengers.split(",")
        passengers_dict = {}

        for passenger in passengers_list:
            key, value = passenger.split(":")
            value = value.strip('[').strip("]").split(";")
            value = [int(v) for v in value]
            passengers_dict[key] = value
        ticket = TicketBooked.objects.create(ticket=ticket, user=request.user)
        for type, ages in passengers_dict.items():
            for age in ages:
                if type == "children":
                    ticket.passengers.create(type=type, age=age)
                else:
                    for i in range(age):
                        ticket.passengers.create(type=type)

        return Response(passengers_dict)
