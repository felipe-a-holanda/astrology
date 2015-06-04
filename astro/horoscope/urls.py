from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('horoscope.views',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'eph/', eph),
    url(r'chart/save/', save_event, name='save_event'),
    url(r'chart/', chart),
    url(r'events/', my_events),
    url(r'test/', test_anguglar),



)