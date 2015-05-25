from django.conf.urls import patterns, url, include

from .api import UserList, UserDetail
from .api import EventList, EventDetail, UserEventList, EphemerisDetail



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

urlpatterns = patterns('',
    url(r'^users/', include(user_urls)),
    url(r'^events/', include(events_urls)),

)
