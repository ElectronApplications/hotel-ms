from decimal import Decimal

from django.core.management.base import BaseCommand

from rest_framework.serializers import ModelSerializer

from hotel.models.client import *
from hotel.models.accomodation import *
from hotel.models.reservation import *
from hotel.models.hotel import *
from hotel.models.gallery import *

import pymongo
from bson.decimal128 import Decimal128


def convert_decimal(dict_item: dict):
    # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
    # Embedded dictionaries and lists are called recursively.
    for k, v in list(dict_item.items()):
        if isinstance(v, dict):
            convert_decimal(v)
        elif isinstance(v, list):
            for l in v:
                convert_decimal(l)
        elif isinstance(v, Decimal):
            dict_item[k] = Decimal128(str(v))


# ACCOMODATION
class AccClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class AccClassSerializer(ModelSerializer):
    class Meta:
        model = ClassInfo
        fields = ["id", "class_description"]


class AccRoomSerializer(ModelSerializer):
    room_class = AccClassSerializer()

    class Meta:
        model = Room
        fields = ["id", "room_class", "room_number", "places"]


class AccReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "move_in_time", "move_out_time", "created_time"]


class AccServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_description"]


class AccServiceCardSerializer(ModelSerializer):
    service = AccServiceSerializer()

    class Meta:
        model = ServiceCard
        fields = [
            "id",
            "service",
            "price_to_pay",
            "service_time",
            "was_price_paid",
            "created_time",
        ]


class AccomodationSerializer(ModelSerializer):
    reservation = AccReservationSerializer()
    client = AccClientSerializer()
    room = AccRoomSerializer()
    servicecards = AccServiceCardSerializer(many=True)

    class Meta:
        model = Accomodation
        fields = "__all__"


# RESERVATION
class ReservationSerializer(ModelSerializer):
    client = AccClientSerializer()
    room = AccRoomSerializer()

    class Meta:
        model = Reservation
        fields = "__all__"


# CLASSINFO
class ClassServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "service_description", "service_price", "gallery"]


class ClassRoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "places"]


class ClassInfoSerializer(ModelSerializer):
    services = ClassServiceSerializer(many=True)
    rooms = ClassRoomSerializer(many=True)

    class Meta:
        model = ClassInfo
        fields = "__all__"


# CLIENT
class ClientAccomodationSerializer(ModelSerializer):
    class Meta:
        model = Accomodation
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    accomodations = ClientAccomodationSerializer(many=True)

    class Meta:
        model = Client
        fields = "__all__"


class Command(BaseCommand):
    help = "Migrate to MongoDB"

    def add_arguments(self, parser):
        parser.add_argument("database", help="MongoDB database")

    def handle(self, *args, **options):
        database: str = options["database"]

        mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
        db = mongoclient[database]

        def export_data(data: list[dict], collection_name: str):
            # db.drop_collection(collection_name)
            # collection = db.create_collection(collection_name)
            collection = db.get_collection(collection_name)
            collection.delete_many({})

            for row in data:
                convert_decimal(row)

            collection.insert_many(data)
            print(f"migrated {collection_name}")

        export_data(
            AccomodationSerializer(Accomodation.objects.all(), many=True).data,
            "accomodation",
        )

        export_data(
            ReservationSerializer(Reservation.objects.all(), many=True).data,
            "reservation",
        )

        export_data(
            ClassInfoSerializer(ClassInfo.objects.all(), many=True).data,
            "classinfo",
        )

        export_data(ClientSerializer(Client.objects.all(), many=True).data, "client")
