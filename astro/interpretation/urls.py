from django.conf.urls import patterns,  url

from .views import *

urlpatterns = patterns('interpretation.views',
    # Examples:
    # url(r'^$', 'apps.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'planet/(?P<planet>\w+)/sign/(?P<sign>\w+)/', planet_in_sign, name='planet_in_sign')


)