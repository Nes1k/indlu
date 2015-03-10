from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourites
from advertisement.models import Advertisement


@login_required
def list_favourites(request):
    favourites, created = Favourites.objects.get_or_create(user=request.user)
    return render(request, 'favourites/list.html', {'favourites': favourites})


@login_required
def add_favourites(request, id):
    instance, created = Favourites.objects.get_or_create(user=request.user)
    try:
        add = Advertisement.objects.get(id=id)
    except:
        pass
    else:
        instance.advertisement.add(add)
        instance.save()

    return redirect('list_favourites')


@login_required
def delete_favourites(request, id):
    instance = get_object_or_404(Favourites, user=request.user)
    try:
        add = Advertisement.objects.get(id=id)
    except:
        pass
    else:
        instance.advertisement.remove(add)
        instance.save()

    return redirect('list_favourites')
