from django.contrib import admin

from hotel.models.accomodation import *
from hotel.models.client import *
from hotel.models.hotel import *
from hotel.models.reservation import *

# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["service_description", "service_price"]
    filter_horizontal = ["classes"]

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ["class_description", "place_price"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "room_class"]

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "status"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "user"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["client", "move_in_time", "move_out_time"]
    filter_horizontal = ["places"]

@admin.register(Accomodation)
class AccomodationAdmin(admin.ModelAdmin):
    list_display = ["client", "move_in_time", "move_out_time", "price_to_pay",
                    "was_price_paid", "checked_out", "reservation"]
    filter_horizontal = ["places"]

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ["service", "accomodation", "price_to_pay", "service_time", "was_price_paid"]