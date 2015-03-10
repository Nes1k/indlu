from django.db.models.signals import post_save
from .models import Advertisement
from stats.models import Stats


def count_statistics(sender, instance, created, *args, **kwargs):
    city = instance.building.city
    buidling_type = instance.building.buidling_type
    advertisement = Advertisement.objects.filter(building__city=city).filter(
        building__buidling_type=buidling_type)
    total_price = 0
    min_ = advertisement.order_by('price')[0].price
    max_ = advertisement.order_by('-price')[0].price
    for add in advertisement:
        total_price += add.price
    average = total_price / advertisement.count()
    stats = Stats(city=city, building_type=buidling_type,
                  max_price=max_, min_price=min_, average_price=average)
    stats.save()


post_save.connect(count_statistics, sender=Advertisement)
