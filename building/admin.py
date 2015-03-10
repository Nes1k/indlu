from django.contrib import admin
from .models import Building, Rooms, Item, RoomImage, Rented


class RoomsInLine(admin.StackedInline):
    model = Rooms
    extra = 1


class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    inlines = [RoomsInLine]


admin.site.register(RoomImage)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Item)
admin.site.register(Rooms)
admin.site.register(Rented)
