from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.accomodation import *
from hotel.serializers.accomodation import *
from hotel.permissions import *

# TODO: let clients make their own accomodations
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
    permission_classes = [IsReception]

# TODO: let clients make their own service orders
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
    permission_classes = [IsReception | IsService]