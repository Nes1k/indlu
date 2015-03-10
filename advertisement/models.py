# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


from building.models import Building, RoomImage, Rooms


TYPE_AD = (
    ('Wynajme', 'Do wynajęcia'),
    ('Sprzedam', 'Na sprzedaż')
)

RATE_OF_PAY = (
    ('Miesięczne', 'Miesięczne'),
    ('Codziennie', 'Codziennie')
)


class Advertisement(models.Model):
    building = models.OneToOneField(Building, verbose_name='Nieruchomość')
    type_advertisement = models.CharField(
        max_length=120, choices=TYPE_AD, verbose_name='Typ')
    payment = models.CharField(
        max_length=120, choices=RATE_OF_PAY, verbose_name='Rozliczanie')
    price = models.IntegerField(default=0, verbose_name='Cena')
    free_places = models.IntegerField(default=0)
    image = models.ForeignKey(RoomImage, verbose_name='Zdjęcie')

    def save(self, *args, **kwargs):
        rooms = self.building.rooms_set.all()
        total = 0
        for room in rooms:
            total += room.free_places
        self.free_places = total
        if not hasattr(self, 'image'):
            for room in rooms:
                if room.roomimage_set.all():
                    self.image = room.roomimage_set.all()[0]
                    break

        super(Advertisement, self).save(*args, **kwargs)

    def get_images_url(self):
        rooms = Rooms.objects.filter(building=self.building)
        images = []
        for room in rooms:
            for image in RoomImage.objects.filter(room=room):
                url = '%s%s' % (settings.MEDIA_URL, image.image)
                images.append(url)
        return images


class Offer(models.Model):
    advertisement = models.ForeignKey(Advertisement, verbose_name='Ogłoszenie')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    accepted = models.BooleanField(default=False, verbose_name='Zaakceptowane')

    def __str__(self):
        return '%s' % self.user.first_name
