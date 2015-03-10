from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm


@login_required
def customer_profile(request):
    user = request.user
    form = CustomerForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
    return render(request, 'customer/profile.html', {'form': form})
