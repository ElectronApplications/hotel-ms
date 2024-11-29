from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Client(models.Model):
    name = models.TextField("ФИО")
    phone_number = models.CharField(
        "Phone number",
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(r"^[+][\d]{7,15}$")
        ]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Role(models.TextChoices):
        CLIENT = "client", "Client"
        RECEPTION = "reception", "Reception staff"
        SERVICE = "service", "Service staff"
        CLEANING = "cleaning", "Cleaning staff"
        PLANNING = "planning", "Plаnning staff"
        ADMIN = "admin", "Admin staff"
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CLIENT)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
@receiver(post_delete, sender=Client)
def delete_django_user(sender, instance: Client, **kwargs):
    instance.user.delete()
