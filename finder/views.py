# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Preferences, Place
from .forms import SearchForm, PreferencesForm, PlaceForm

from advertisement.models import Advertisement, Offer
from stats.models import Stats


def home(request):
    advertisement = Advertisement.objects.all()
    form = SearchForm(data=request.GET)
    if request.GET.get('city'):
        advertisement = advertisement.filter(
            building__city__startswith=request.GET['city'])
    if request.GET.get('places'):
        if request.GET['places'] == '5':
            advertisement = advertisement.filter(free_places__gte=5)
        elif request.GET['places'] != '5' and request.GET['places'] != '0':
            advertisement = advertisement.filter(
                free_places=request.GET['places'])
    if request.GET.get('buidling_type'):
        advertisement = advertisement.filter(
            building__buidling_type=request.GET['buidling_type'])
    if request.GET.get('payment'):
        advertisement = advertisement.filter(
            payment__contains=request.GET['payment'])
    if request.GET.get('min_price'):
        advertisement = advertisement.filter(
            price__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        advertisement = advertisement.filter(
            price__lte=request.GET['max_price'])
    if request.GET.get('sort_by'):
        if request.GET['sort_by'] == '1':
            advertisement = advertisement.order_by('-price')
        if request.GET['sort_by'] == '2':
            advertisement = advertisement.order_by('price')

    return render(request, 'finder/home.html',
                  {'title': 'Znajdź dla siebie idealne mieszkanie',
                   'advertisement': advertisement, 'form': form})


def search_panel(request):
    preferences, created = Preferences.objects.get_or_create(user=request.user)
    preferences_form = PreferencesForm(
        request.POST or None, instance=preferences)
    if preferences_form.is_valid():
        preferences_form.save()

    stats = Stats.objects.filter(city=preferences.city)[25:]
    places = Place.objects.filter(preferences=preferences)
    offers = Offer.objects.filter(user=request.user)
    # TODO: Add support for matching advertisement

    return render(request, 'finder/search_panel.html',
                  {'preferences_form': preferences_form, 'stats': stats,
                   'places': places, 'offers': offers})


def add_place(request):
    preferences = Preferences.objects.get(user=request.user)
    form = PlaceForm()
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.preferences = preferences
            place.save()
            messages.success(
                request, "%s, %s zostało dodane do listy miejsc." % (place.city, place.street))
            return redirect('search_panel')

    return render(request, 'finder/configure_place.html', {'form': form})


def edit_place(request, id):
    place = get_object_or_404(Place, preferences__user=request.user, id=id)
    form = PlaceForm(request.POST or None, instance=place)
    if form.is_valid():
        form.save()
        return redirect('search_panel')

    return render(request, 'finder/configure_place.html', {'form': form})


def delete_place(request, id):
    place = get_object_or_404(Place, preferences__user=request.user, id=id)
    place.delete()
    messages.success(
        request, "%s, %s zostało usunięte z listy miejsc." (place.city, place.street))
    return redirect('search_panel')
