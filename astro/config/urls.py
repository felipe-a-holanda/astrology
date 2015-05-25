from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'horoscope.views.home'),
    url(r'^geocode/$', 'horoscope.views.geocode'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^api/', include('api.urls')),
    url(r'^horoscope/', include('horoscope.urls')),
    url(r'^interpretation/', include('interpretation.urls')),


)
