from django.db.models.signals import post_save
from .models import Rooms, RoomImage

from .utils import resize_and_crop


def resize(sender, instance, created, *args, **kwargs):
        # Resize and crop all upload image.
    resize_and_crop(instance.image.path, (1600, 900))

post_save.connect(resize, sender=RoomImage)


def recount(sender, instance, created, *args, **kwargs):
        # If building has advertisement then recount: free places
        # and realty area
    if hasattr(instance.building, 'advertisement'):
        instance.building.advertisement.save()
    instance.building.save()


post_save.connect(recount, sender=Rooms)
