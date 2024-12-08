from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from hotel.models.client import *
from hotel.serializers.client import *
from hotel.permissions import *

class UserViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_object(self):
        return self.get_queryset().first()

    @action(detail=False, url_path="self", methods=["get"], permission_classes=[IsAuthenticated])
    def get_self(self, request, *args, **kwargs):
        client = self.get_queryset().first()
        serializer = self.get_serializer(client)
        return Response(serializer.data)

    @action(detail=False, url_path="update-self", methods=["put"], permission_classes=[IsAuthenticated], serializer_class=UpdateUserSerializer)
    def update_self(self, request, *args, **kwargs):
        client = self.get_queryset().first()
        serializer = self.get_serializer(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=False, url_path="password", methods=["put"], permission_classes=[IsAuthenticated], serializer_class=UserChangePasswordSerializer)
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Client.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["role"]
    search_fields = ["name", "phone_number"]
    permission_classes = [IsReception]

    def get_serializer_class(self):
        if IsAdmin().has_permission(self.request, self):
            return AdminClientSerializer
        else:
            return ClientSerializer

    def check_object_permissions(self, request, obj: Client):
        super().check_object_permissions(request, obj)

        if obj.role == Client.Role.ADMIN:
            self.permission_denied(request, "Can't modify admins")
        
        if obj.role != Client.Role.CLIENT and not IsAdmin().has_permission(request, self):
            self.permission_denied(request, "Reception can only modify normal clients")