# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Advertisement, Offer
from .forms import AdvertisementForm

from building.models import Building
from stats.models import Stats

from customer.forms import PrimaryContactForm


def profile(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)
    stats = Stats.objects.filter(
        city=advertisement.building.city).order_by('-time')[:20]
    # TODO: Repair stats
    stats = reversed(stats)

    return render(request, 'advertisement/profile.html', {'advertisement': advertisement, 'stats': stats})


@login_required
def add_advertisement(request, id):
    primarycontact_form = PrimaryContactForm(
        request.POST or None, instance=request.user)
    if primarycontact_form.is_valid():
        primarycontact_form.save()
    building = get_object_or_404(Building, id=id, user=request.user)
    form = AdvertisementForm(initial={'building': building})
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Twoje ogłoszenie zostało dodane.')
            return redirect('manage_building', building.id)

    return render(request, 'advertisement/configure.html',
                  {'form': form, 'edit': False, 'building_id': building.id,
                   'primarycontact_form': primarycontact_form})


@login_required
def edit_advertisement(request, id):
    primarycontact_form = PrimaryContactForm(
        request.POST or None, instance=request.user)
    if primarycontact_form.is_valid():
        primarycontact_form.save()
    advertisement = get_object_or_404(
        Advertisement, id=id, building__user=request.user)
    form = AdvertisementForm(request.POST or None, instance=advertisement)
    if form.is_valid():
        form.save()
        return redirect('manage_building', advertisement.building.id)

    return render(request, 'advertisement/configure.html',
                  {'form': form, 'edit': True, 'building_id': advertisement.building.id,
                   'primarycontact_form': primarycontact_form})


@login_required
def delete_advertisement(request, id):
    advertisement = get_object_or_404(
        Advertisement, id=id, building__user=request.user)
    advertisement.delete()

    return redirect('manage_building', advertisement.building.id)


@login_required
def add_offer(request, id):
    advertisement = get_object_or_404(Advertisement, id=id)
    offer = Offer(advertisement=advertisement, user=request.user)
    offer.save()
    messages.success(
        request, 'Wysłałeś swoją ofertę na nieruchomość')

    return redirect('search_panel')


@login_required
def delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id, user=request.user)
    offer.delete()
    messages.success(
        request, 'Usunąłeś swoją, ofertę.')

    return redirect('search_panel')


@login_required
def accept_offer(request, id):
    # TODO: Implement support for rent.
    messages.success(request, 'Zaakceptowałeś, ofertę %s')

    return redirect('manage_building')


@login_required
def reject_offer(request, id):
    offer = get_object_or_404(
        Offer, id=id, advertisement__building__user=request.user)
    offer.delete()
    messages.success(request, 'Odrzuciłeś, ofertę %s' % offer.user.first_name)

    return redirect('manage_building', offer.advertisement.building.id)
