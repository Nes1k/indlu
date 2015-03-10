from django.conf.urls import patterns, url

urlpatterns = patterns(
    'finder.views',
    url(r'^$', 'search_panel', name='search_panel'),
    url(r'^place/add$', 'add_place', name='add_place'),
    url(r'^place/(?P<id>\d+)/edit$', 'edit_place', name='edit_place'),
    url(r'^place/(?P<id>\d+)/delete$', 'delete_place', name='delete_place'),
)
