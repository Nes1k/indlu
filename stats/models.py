from django.db import models


class Stats(models.Model):
    city = models.CharField(max_length=40)
    building_type = models.CharField(max_length=40)
    max_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    min_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    average_price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.average_price
