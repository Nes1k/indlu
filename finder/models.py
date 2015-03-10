# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models

from geopy import geocoders

from advertisement.models import RATE_OF_PAY
from building.models import BUILDING_TYPE

PLACES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 'więcej'))

# TODO: Add mixins to preferences and building.


class Preferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1)
    city = models.CharField(
        max_length=120, blank=True, null=True, verbose_name='Miasto')
    places = models.IntegerField(
        default=0, blank=True, null=True, choices=PLACES, verbose_name='Liczba miejsc')
    buidling_type = models.CharField(
        max_length=120, choices=BUILDING_TYPE, blank=True, null=True, verbose_name='Typ budynku')
    payment = models.CharField(
        max_length=120, choices=RATE_OF_PAY, blank=True, null=True, verbose_name='Płatności')
    min_price = models.IntegerField(
        blank=True, null=True, verbose_name='Minimalna cena')
    max_price = models.IntegerField(
        blank=True, null=True, verbose_name='Maksymalna cena')


class Place(models.Model):
    preferences = models.ForeignKey(Preferences)
    city = models.CharField(
        max_length=120, blank=True, null=True, verbose_name='Miasto')
    street = models.CharField(
        max_length=120, blank=True, null=True, verbose_name='Ulica')
    distance = models.DecimalField(
        default=0, max_digits=4, decimal_places=2, verbose_name="Odległość")
    location = gis_models.PointField(
        'longitude/latitude', geography=True, blank=True, null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        g = geocoders.GoogleV3(domain='maps.google.pl')
        location = g.geocode('%s, %s' % (self.city, self.street))
        if location is not None:
            point = "POINT (%s %s)" % (location.latitude, location.longitude)
            self.location = point
        super(Place, self).save(*args, **kwargs)

    def __str__(self):
        return self.city
