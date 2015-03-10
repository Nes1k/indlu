from django.conf.urls import patterns, url

urlpatterns = patterns(
    'customer.views',
    url(r'^$', 'customer_profile', name='customer_profile'),
)
