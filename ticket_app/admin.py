from django.contrib import admin
from . import models


# Register your models here.

class PassengerInLine(admin.TabularInline):
    model = models.Passengers


@admin.register(models.TicketBooked)
class TicketBookedAdmin(admin.ModelAdmin):
    inlines = [PassengerInLine]


admin.site.register(models.Airline)
admin.site.register(models.Ticket)
