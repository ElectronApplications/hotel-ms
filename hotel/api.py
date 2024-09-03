from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models import Client, Reservation
from hotel.serializers import ClientSerializer, ReservationSerializer

class ClientsViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ReservationsViewSet(
    mixins.ListModelMixin, 
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer