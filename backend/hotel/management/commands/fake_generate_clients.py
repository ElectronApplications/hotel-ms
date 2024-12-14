from django.core.management.base import BaseCommand

from faker import Faker

from hotel.models.client import *

class Command(BaseCommand):
    help = "Creates a bunch of fake clients"

    def add_arguments(self, parser):
        parser.add_argument("count", help="The amount of fake clients")
        parser.add_argument("--locale", help="Data locale", default="ru_RU")

    def handle(self, *args, **options):
        fake = Faker([options["locale"]])

        for _ in range(int(options["count"])):
            client = Client.objects.create(
                name=fake.name(),
                phone_number=f"+{fake.msisdn()}"
            )
