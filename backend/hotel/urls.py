from rest_framework.routers import BaseRouter

from hotel.views.client import *
from hotel.views.gallery import *
from hotel.views.hotel import *
from hotel.views.reservation import *
from hotel.views.accomodation import *
from hotel.views.stats import *

def register_hotel_routes(router: BaseRouter):
    router.register("gallery", GalleryViewSet)

    router.register("user", UserViewSet, "user")
    router.register("client", ClientViewSet, "client")
    
    router.register("class", ClassInfoViewSet)
    router.register("room", RoomViewSet)
    router.register("service", ServiceViewSet)
    
    router.register("reservation", ReservationViewSet)
    
    router.register("accomodation", AccomodationViewSet)
    router.register("servicecard", ServiceCardViewSet)
    
    router.register("stats", StatsViewset, "stats")