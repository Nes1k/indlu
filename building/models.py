# -*- coding: utf-8 -*-
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.conf import settings
from geopy import geocoders
from customer.models import COUNTRIES

ROOMS_TYPE = (
    ('1', 'Pokój'),
    ('2', 'Kuchnia'),
    ('3', 'Łazienka'),
    ('4', 'Hall'),
    ('5', 'Pokój + Kuchnia')
)

BUILDING_TYPE = (
    ('Dom', 'Dom'),
    ('Blok', 'Blok'),
    ('Kamienica', 'Kamienica'),
    ('Apartamentowiec', 'Apartamentowiec')
)


class RoomImage(models.Model):
    room = models.ForeignKey('Rooms')
    image = models.ImageField(upload_to='room/')

    def __str__(self):
        return self.room.name


class Item(models.Model):
    name = models.CharField(max_length=120)
    where = models.CharField(max_length=120, default=None, choices=ROOMS_TYPE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['where']


class Rooms(models.Model):
    rooms_type = models.CharField(
        max_length=120, choices=ROOMS_TYPE, verbose_name='Typ pomieszczenia')
    name = models.CharField(max_length=120, verbose_name='Nazwa')
    area = models.DecimalField(
        default=0, blank=False, max_digits=4, decimal_places=2, verbose_name='Powieżchnia')
    free_places = models.IntegerField(default=0, verbose_name='Wolnych miejsc')
    building = models.ForeignKey('Building')
    equipment = models.ManyToManyField(Item, verbose_name='Wyposażenie')

    def __str__(self):
        return self.name

    def get_image_url(self):
        try:
            image = RoomImage.objects.filter(room=self.id)[0]
        except:
            return None
        else:
            return "%s/%s" % (settings.MEDIA_URL, image.image)


class Building(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    country = models.CharField(max_length=120, choices=COUNTRIES, verbose_name="Kraj")
    street_address = models.CharField(max_length=120, verbose_name='Ulica')
    postal_code = models.CharField(max_length=120, verbose_name='Kod pocztowy')
    city = models.CharField(max_length=120, verbose_name='Miasto')
    buidling_type = models.CharField(max_length=120, choices=BUILDING_TYPE, verbose_name='Typ budynku')
    name = models.CharField(max_length=120, verbose_name='Nazwa budynku')
    area = models.DecimalField(
        default=0, blank=False, max_digits=4, decimal_places=2, verbose_name='Powieżchnia')
    total_places = models.IntegerField(default=0, verbose_name='Liczba miejsc')
    location = gis_models.PointField(
        'longitude/latitude', geography=True, blank=True, null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        g = geocoders.GoogleV3(domain='maps.google.pl')
        location = g.geocode('%s, %s' % (self.city, self.street_address))
        if location is not None:
            point = "POINT (%s %s)" % (location.latitude, location.longitude)
            self.location = point
        rooms = Rooms.objects.filter(building=self.id)
        total = 0
        for room in rooms:
            total += room.area
        self.area = total
        super(Building, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_image_url(self):
        try:
            image = RoomImage.objects.filter(room__building=self.id)[0]
        except:
            return None
        else:
            return "%s/%s" % (settings.MEDIA_URL, image.image)

    def room_count(self):
        number = Rooms.objects.filter(building=self.id).count()
        return "%s" % number


class Rented(models.Model):
    building = models.OneToOneField(Building)
    tenants = models.OneToOneField(settings.AUTH_USER_MODEL)
