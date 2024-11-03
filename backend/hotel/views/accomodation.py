from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.accomodation import *
from hotel.serializers.accomodation import *

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