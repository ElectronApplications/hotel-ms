from django.db import models

from hotel.models.client import Client
from hotel.models.hotel import Place

class Reservation(models.Model):
    move_in_time = models.DateTimeField("Time of moving in")
    move_out_time = models.DateTimeField("Time of moving out")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name="reservations")
    places = models.ManyToManyField(Place, related_name="reservations")

    def __str__(self) -> str:
        return f"Reservation №{self.id} for {self.client.name}"

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
