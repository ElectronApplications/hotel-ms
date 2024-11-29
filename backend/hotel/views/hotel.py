from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from hotel.models.hotel import *
from hotel.serializers.hotel import *
from hotel.permissions import *

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
    permission_classes = [IsPlanningOrReadOnly]

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
    permission_classes = [IsPlanningOrReadOnly]

class PlaceViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Place.objects.all()
    permission_classes = [IsPlanningOrReadOnly | IsCleaningOrReadOnly]

    def get_serializer_class(self):
        if IsCleaning().has_permission(self.request, self) and not IsAdmin().has_permission(self.request, self):
            return CleaningPlaceSerializer
        else:
            return PlaceSerializer

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
    permission_classes = [IsPlanningOrReadOnly]