"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import include, path

from hotel import views
from hotel.api import ClientsViewSet, ReservationsViewSet

router = DefaultRouter()
router.register("clients", ClientsViewSet, basename="clients")
router.register("reservations", ReservationsViewSet, basename="reservations")

urlpatterns = [
    path('', views.ShowClientsView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]