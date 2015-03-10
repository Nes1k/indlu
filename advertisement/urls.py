from django.conf.urls import patterns, url

urlpatterns = patterns(
    'advertisement.views',
    url(r'^(?P<id>\d+)$', 'profile', name="profile_advertisement"),
    url(r'^(?P<id>\d+)/add/$', 'add_advertisement', name="add_advertisement"),
    url(r'^(?P<id>\d+)/edit/$', 'edit_advertisement', name="edit_advertisement"),
    url(r'^(?P<id>\d+)/delete/$', 'delete_advertisement', name="delete_advertisement"),

    url(r'^(?P<id>\d+)/offer/add$', 'add_offer', name="add_offer"),
    url(r'^offer/(?P<id>\d+)/delete$', 'delete_offer', name="delete_offer"),
    url(r'^offer/(?P<id>\d+)/reject$', 'reject_offer', name="reject_offer"),
)
