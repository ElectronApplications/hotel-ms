from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.TextField("Номер телефона")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Reservation(models.Model):
    move_in_time = models.DateTimeField("Время въезда")
    move_out_time = models.DateTimeField("Время выезда")
    client = models.ForeignKey("Client", on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"