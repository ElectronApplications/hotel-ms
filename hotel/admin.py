from django.contrib import admin

from hotel.models import Client, Reservation

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["client", "move_in_time", "move_out_time"]