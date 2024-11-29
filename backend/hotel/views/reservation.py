from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.reservation import *
from hotel.serializers.reservation import *
from hotel.permissions import *

# TODO: let clients make their own reservations
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
    permission_classes = [IsReception]