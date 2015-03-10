from django.conf.urls import patterns, url
urlpatterns = patterns(
    'building.views',
    url(r'^$', 'all_building', name='all_building'),
    url(r'^add/$', 'add_building', name='add_building'),
    url(r'^(?P<id>\d+)/edit$', 'edit_building', name='edit_building'),
    url(r'^(?P<id>\d+)/manage$', 'manage_building', name='manage_building'),
    url(r'^(?P<id>\d+)/delete$', 'delete_building', name='delete_building'),

    url(r'^(?P<id>\d+)/add-locators/(?P<user_id>\d+)/$', 'add_locators', name='add_locators'),
    url(r'^(?P<id>\d+)/delete-locators/$', 'delete_locators', name='delete_locators'),

    url(r'^(?P<id>\d+)/room/add$', 'add_room', name='add_room'),
    url(r'^(?P<id>\d+)/room/(?P<room_id>\d+)/$', 'edit_room', name='edit_room'),
    url(r'^room/(?P<id>\d+)/delete$', 'delete_room', name='delete_room'),
)
