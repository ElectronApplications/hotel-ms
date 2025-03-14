from django.db import models

from hotel.models.client import Client
from hotel.models.hotel import Room

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, related_name="reservations")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name="reservations")
    move_in_time = models.DateTimeField("Time of moving in")
    move_out_time = models.DateTimeField("Time of moving out")
    created_time = models.DateTimeField("Accomodation creation time", auto_now=True)

    def __str__(self) -> str:
        return f"Reservation №{self.id} for {self.client.name}"

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
