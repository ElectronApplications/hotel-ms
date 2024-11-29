from rest_framework import permissions
from hotel.models.client import Client

def get_client(request) -> Client | None:
    if request.user is None or not request.user.is_authenticated:
        return None
    else:
        return Client.objects.filter(user=request.user).first()

class IsReception(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.RECEPTION or client.role == Client.Role.ADMIN))

class IsReceptionOrReadOnly(IsReception):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))


class IsService(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.SERVICE or client.role == Client.Role.ADMIN))

class IsServiceOrReadOnly(IsService):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))


class IsCleaning(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.CLEANING or client.role == Client.Role.ADMIN))

class IsCleaningOrReadOnly(IsCleaning):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))
    

class IsPlanning(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.PLANNING or client.role == Client.Role.ADMIN))

class IsPlanningOrReadOnly(IsPlanning):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and client.role == Client.Role.ADMIN)

class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or super().has_permission(request, view))