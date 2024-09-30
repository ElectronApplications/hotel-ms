from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from hotel.models.client import Client

# Create your views here.

class ShowClientsView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        clients = Client.objects.all()
        
        result = ""
        for client in clients:
            result += str(client) + "<br>"

        return HttpResponse(result)