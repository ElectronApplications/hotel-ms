from django.contrib import admin

from hotel.models.accomodation import *
from hotel.models.client import *
from hotel.models.gallery import *
from hotel.models.hotel import *
from hotel.models.reservation import *

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["image", "gallery"]

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["service_description", "service_price", "gallery"]
    filter_horizontal = ["classes"]

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ["class_description", "place_price", "gallery"]

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["room_number", "room_class", "status", "places"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number", "role", "user"]

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["client", "room", "move_in_time", "move_out_time"]

@admin.register(Accomodation)
class AccomodationAdmin(admin.ModelAdmin):
    list_display = ["client", "room", "move_in_time", "move_out_time", "price_to_pay",
                    "was_price_paid", "checked_out", "reservation"]

@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ["service", "accomodation", "price_to_pay", "service_time", "was_price_paid"]