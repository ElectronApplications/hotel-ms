from rest_framework.routers import BaseRouter

from hotel.api import *
from hotel.views.client import ClientViewSet

def register_hotel_routes(router: BaseRouter):
    router.register("client", ClientViewSet)
    
    router.register("class", ClassInfoViewSet)
    router.register("room", RoomViewSet)
    router.register("place", PlaceViewSet)
    router.register("service", ServiceViewSet)
    router.register("reservation", ReservationViewSet)
    router.register("accomodation", AccomodationViewSet)
    router.register("servicecard", ServiceCardViewSet)