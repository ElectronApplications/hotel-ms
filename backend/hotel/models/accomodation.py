from django.db import models

from hotel.models.client import Client
from hotel.models.hotel import Room, Service
from hotel.models.reservation import Reservation

class Accomodation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name="accomodations")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name="accomodations")
    price_to_pay = models.DecimalField("Accomodation's price", max_digits=8, decimal_places=2)
    move_in_time = models.DateTimeField("Time of moving in")
    move_out_time = models.DateTimeField("Time of moving out")
    was_price_paid = models.BooleanField("Did the client pay", default=False)
    checked_out = models.BooleanField("Did the client check out", default=False)
    reservation = models.OneToOneField(Reservation, on_delete=models.SET_NULL, null=True, blank=True, related_name="accomodation")

    def __str__(self) -> str:
        return f"Accomodation №{self.id} for {self.client.name}"

    class Meta:
        verbose_name = "Accomodation"
        verbose_name_plural = "Accomodations"

class ServiceCard(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=False, related_name="servicecards")
    accomodation = models.ForeignKey(Accomodation, on_delete=models.CASCADE, null=False, related_name="servicecards")
    price_to_pay = models.DecimalField("Service's price", max_digits=8, decimal_places=2)
    service_time = models.DateTimeField("Time of service")
    was_price_paid = models.BooleanField("Did the client pay", default=False)

    def __str__(self) -> str:
        return f"Service card №{self.id} for {self.accomodation.client.name} and accomodation №{self.accomodation.id}"

    class Meta:
        verbose_name = "Service card"
        verbose_name_plural = "Service cards"