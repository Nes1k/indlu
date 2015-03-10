from django.contrib import admin
from .models import Stats


class AdminStats(admin.ModelAdmin):
    list_display = ['city', 'average_price']

admin.site.register(Stats, AdminStats)
