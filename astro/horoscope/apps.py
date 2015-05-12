from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class HoroscopeConfig(AppConfig):
    name = 'horoscope'
    verbose_name = _('Horoscope')