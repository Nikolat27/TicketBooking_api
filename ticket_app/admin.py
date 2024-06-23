from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Airline)
admin.site.register(models.Ticket)