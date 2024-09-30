from django.db import models

from hotel.models.client import Client
from hotel.models.place import Place
from hotel.models.reservation import Reservation
from hotel.models.service import Service

class Accomodation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name="accomodations")
    price_to_pay = models.DecimalField("Стоимость проживания", max_digits=8, decimal_places=2)
    move_in_time = models.DateTimeField("Время въезда")
    move_out_time = models.DateTimeField("Время выезда")
    was_price_paid = models.BooleanField("Оплачено ли проживание", default=False)
    checked_out = models.BooleanField("Уже выехали", default=False)
    places = models.ManyToManyField(Place, related_name="accomodations")
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True, related_name="accomodation")

    class Meta:
        verbose_name = "Проживание"
        verbose_name_plural = "Проживания"

class ServiceCard(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False, related_name="servicecards")
    accomodation = models.ForeignKey(Accomodation, on_delete=models.CASCADE, null=False, related_name="servicecards")
    price_to_pay = models.DecimalField("Стоимость услуги", max_digits=8, decimal_places=2)
    service_time = models.DateTimeField("Время предоставления услуги")
    was_price_paid = models.BooleanField("Оплачена ли услуга", default=False)

    class Meta:
        verbose_name = "Карточка услуг"
        verbose_name_plural = "Карточки услуг"