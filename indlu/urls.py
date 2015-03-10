from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', 'finder.views.home', name='home'),
    url(r'^advertisement/', include('advertisement.urls')),
    url(r'^realty/', include('building.urls')),
    url(r'^favourites/', include('favourites.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^finder/', include('finder.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }),
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT,
                            }),
                            )
