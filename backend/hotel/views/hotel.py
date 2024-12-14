from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["class_description", "place_price"]
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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "room_class"]
    ordering_fields = ["room_number", "places"]
    serializer_class = RoomSerializer
    permission_classes = [IsPlanningOrReadOnly | IsCleaningOrReadOnly]

    def get_serializer_class(self):
        if IsCleaning().has_permission(self.request, self) and not IsAdmin().has_permission(self.request, self):
            return CleaningRoomSerializer
        else:
            return RoomSerializer
    
class ServiceViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Service.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["service_description", "service_price"]
    serializer_class = ServiceSerializer
    permission_classes = [IsPlanningOrReadOnly]