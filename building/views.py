# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Building, Rooms, RoomImage, Rented
from .forms import BuildingForm, RoomForm, ImageForm

from advertisement.models import Offer


@login_required
def all_building(request):
    try:
        buildings = Building.objects.filter(user=request.user)
    except:
        buildings = False
    return render(request, 'building/all.html', {'title': 'Zarządzaj mieszkaniami', 'buildings': buildings})


@login_required
def manage_building(request, id):
    building = get_object_or_404(Building, id=id, user=request.user)
    if hasattr(building, 'advertisement'):
        offers = Offer.objects.filter(advertisement__building=building)
    else:
        offers = None
    # TODO: Implement support for rent.
    if hasattr(building, 'rented'):
        tenants = Rented.objects.get(realty=building).tenants
    else:
        tenants = None
    return render(request, 'building/manage.html', {'building': building, 'offers': offers, 'tenants': tenants})


@login_required
def add_building(request):
    form = BuildingForm()
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.user = request.user
            building.save()
            messages.success(
                request, 'Nieruchomość %s została dodana do systemu. Możesz nią teraz zarządzać. ' % (building.name))
            return redirect('edit_building', building.id)
    return render(request, 'building/configure_realty.html', {'form': form, 'add': True})


@login_required
def edit_building(request, id):
    building = get_object_or_404(Building, id=id, user=request.user)
    form = BuildingForm(request.POST or None, instance=building)
    if form.is_valid():
        form.save()
    return render(request, 'building/configure_realty.html', {'building': building, 'form': form})


def delete_building(request, id):
    building = get_object_or_404(Building, id=id, user=request.user)
    building.delete()
    messages.success(
        request, 'Nieruchomość %s została usunięta z systemu.' % (building.name))
    return redirect('all_building')


@login_required
def add_room(request, id):
    building = get_object_or_404(Building, id=id, user=request.user)
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.building = building
            room.save()
            imgForm = ImageForm(request.POST, request.FILES)
            if imgForm.is_valid():
                instance = RoomImage(
                    room=room, image=imgForm.cleaned_data['image'])
                instance.save()
            return redirect('edit_building', building.id)
    return render(request, 'building/configure_room.html', {'form': form, 'id': id})


@login_required
def edit_room(request, id, room_id):
    room = get_object_or_404(Rooms, id=room_id, building__user=request.user)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        imgForm = ImageForm(request.POST, request.FILES)
        if imgForm.is_valid():
            instance = RoomImage(
                room=room, image=imgForm.cleaned_data['image'])
            instance.save()
    return render(request, 'building/configure_room.html', {'form': form, 'id': id, 'room': room})


@login_required
def delete_room(request, id):
    room = get_object_or_404(Rooms, id=id, building__user=request.user)
    room.delete()
    messages.success(
        request, 'Pokój %s została usunięty z tej nieruchomości. ' % (room.name))
    return redirect('edit_building', room.building.id)


@login_required
def add_locators(request, id, user_id):
    building = get_object_or_404(Building, id=id, user=request.user)
    offer = get_object_or_404(
        Offer, advertisement__building=building, user=user_id)
    rented, created = Rented.objects.get_or_create(building=building)
    rented.tenants.add(request.user)
    offer.delete()
    return redirect('manage_building', building.id)


@login_required
def delete_locators(request, id):
    building = get_object_or_404(Building, id=id, user=request.user)
    return redirect('manage_building', building.id)
