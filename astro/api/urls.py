from django.conf.urls import patterns, url, include

from .api import UserList, UserDetail, UserEventList
from .api import EventList, EventDetail, EphemerisDetail
from .api import LocationList, LocationDetail



user_urls = patterns('',
    url(r'^(?P<pk>[0-9]+)/events/', UserEventList.as_view(), name='user-event-list'),
    url(r'^(?P<pk>[0-9]+)/', UserDetail.as_view(), name='user-detail'),
    url(r'^$', UserList.as_view(), name='user-list'),



)

events_urls = patterns('',
    url(r'^(?P<pk>\d+)/ephemeris/$', EphemerisDetail.as_view(), name='ephemeris-detail'),
    url(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='event-detail'),
    url(r'^$', EventList.as_view(), name='event-list')
)

location_urls = patterns('',
    url(r'^(?P<pk>\d+)/$', LocationDetail.as_view(), name='location-detail'),
    url(r'^$', LocationList.as_view(), name='location-list')
)

urlpatterns = patterns('',
    url(r'^users/', include(user_urls)),
    url(r'^events/', include(events_urls)),
    url(r'^location/', include(location_urls)),

)
