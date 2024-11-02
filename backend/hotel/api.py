from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.accomodation import Accomodation, ServiceCard
from hotel.models.service import Service
from hotel.models.place import ClassInfo, Place, Room
from hotel.models.reservation import Reservation
from hotel.serializers import AccomodationSerializer, ClassInfoSerializer, PlaceSerializer, ReservationSerializer, RoomSerializer, ServiceCardSerializer, ServiceSerializer

# TODO: actual logic for interacting with the models (not to mention authorization)

class ClassInfoViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ClassInfo.objects.all()
    serializer_class = ClassInfoSerializer

class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class PlaceViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class ServiceViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class AccomodationViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Accomodation.objects.all()
    serializer_class = AccomodationSerializer

class ServiceCardViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ServiceCard.objects.all()
    serializer_class = ServiceCardSerializer