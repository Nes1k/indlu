from django.db import models
from django.conf import settings

from advertisement.models import Advertisement


class Favourites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    advertisement = models.ManyToManyField(Advertisement)
