from rest_framework import permissions
from hotel.models.client import Client

def get_client(request) -> Client | None:
    if request.user is None:
        return None
    else:
        return Client.objects.filter(user=request.user).first()

class IsReception(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.RECEPTION or client.role == Client.Role.ADMIN))

class IsService(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.SERVICE or client.role == Client.Role.ADMIN))

class IsCleaning(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.CLEANING or client.role == Client.Role.ADMIN))

class IsPlanning(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and (client.role == Client.Role.PLANNING or client.role == Client.Role.ADMIN))

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        client = get_client(request)
        return bool(client and client.role == Client.Role.ADMIN)