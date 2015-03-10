from django.conf.urls import patterns, url

urlpatterns = patterns(
    'favourites.views',
    url(r'^$', 'list_favourites', name='list_favourites'),
    url(r'^(?P<id>\d+)/add/$', 'add_favourites', name='add_favourites'),
    url(r'^(?P<id>\d+)/delete/$', 'delete_favourites', name='delete_favourites'),
)
