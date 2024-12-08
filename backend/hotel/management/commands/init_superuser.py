from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from hotel.models.client import Client

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--phone_number', help="Admin's phone number", required=True)
        parser.add_argument('--password', help="Admin's password", required=True)

    def handle(self, *args, **options):
        phone_number = options["phone_number"]

        user = User.objects.filter(username=phone_number).first()
        if user is None:
            user = User.objects.create_superuser(username=phone_number, password=options['password'])
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        print(f"Created/updated superuser {phone_number}")
        
        client = Client.objects.filter(user=user).first()
        if client is None:
            Client.objects.create(name=phone_number, phone_number=phone_number, user=user, role=Client.Role.ADMIN)
        else:
            client.role = Client.Role.ADMIN
            client.save()
        print(f"Created/updated admin client {phone_number}")
