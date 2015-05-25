from django.conf.urls import patterns, url, include

from .api import UserList, UserDetail
from .api import EventList, EventDetail, UserEventList, EphemerisDetail



user_urls = patterns('',
    url(r'^(?P<username>[0-9a-zA-Z_-]+)/events/', UserEventList.as_view(), name='userevent-list'),
    url(r'^(?P<username>[0-9a-zA-Z_-]+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^$', UserList.as_view(), name='user-list')
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
