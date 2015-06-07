from dateutil.parser import parse
import pytz
import geocoder
import swisseph as swe
swe.set_ephe_path('/usr/share/libswe/ephe/')

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.db import models
from timezone_field import TimeZoneField
from tzwhere.tzwhere import tzwhere
from users.models import UserProfile

tzwhere = tzwhere()

class Event(models.Model):
    user = models.ForeignKey(UserProfile, related_name='events', null=True, verbose_name=_('User'))
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    date = models.DateTimeField(verbose_name=_('Date'))
    city = models.CharField(max_length=256, verbose_name=_('City'))

    location = models.ForeignKey('Location', related_name='events', null=True, verbose_name=_('Location'))
    ephemeris = models.OneToOneField('Ephemeris', related_name='event', verbose_name=_('Events'))
    houses = models.OneToOneField('Houses', related_name='event', verbose_name=_('Houses'))

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def save(self, *args, **kwargs):
        if not self.location:
            self.location = Location.create(self.city)
        if not self.ephemeris:
            self.ephemeris = Ephemeris.create(self.date)
        if not self.houses:
            self.houses = Houses.create(self.date, self.location.lat, self.location.lng)
        super(Event, self).save(*args, **kwargs)

    @classmethod
    def create(cls, name, date, time, location):
        location = Location.create(location)

        naive_date = parse("%s %s" % (date, time))
        datetime = location.timezone.localize(naive_date)
        datetime_utc = datetime.astimezone(pytz.utc)

        ephemeris = Ephemeris.create(datetime_utc)
        ephemeris.save()

        houses = Houses.create(datetime_utc, location.lat, location.lng)

        self = cls()
        self.name = name
        self.date = datetime_utc
        self.city = "%s (%s)" % (location.city, location.country)
        self.ephemeris = ephemeris
        self.location = location
        self.houses = houses
        self.save()
        return self



def julday(d):
    j = swe.julday(d.year, d.month, d.day, d.hour + d.minute/60.0)
    return j




class Ephemeris(models.Model):
    N_PLANETS = 23

    sun = models.FloatField(_('Sun'))
    moon = models.FloatField(_('Moon'))
    mercury = models.FloatField(_('Mercury'))
    venus = models.FloatField(_('Venus'))
    mars = models.FloatField(_('Mars'))
    jupiter = models.FloatField(_('Jupiter'))
    saturn = models.FloatField(_('Saturn'))
    uranus = models.FloatField(_('Uranus'))
    neptune = models.FloatField(_('Neptune'))
    pluto = models.FloatField(_('Pluto'))

    mean_node = models.FloatField()
    true_node = models.FloatField()
    mean_apog = models.FloatField()
    oscu_apog = models.FloatField()
    earth = models.FloatField()
    chiron = models.FloatField()
    pholus = models.FloatField()
    ceres = models.FloatField()
    pallas = models.FloatField()
    juno = models.FloatField()
    vesta = models.FloatField()
    intp_apog = models.FloatField()
    intp_perg = models.FloatField()

    class Meta:
        verbose_name = pgettext_lazy('singular', 'ephemeris')
        verbose_name_plural = pgettext_lazy('plural', 'ephemeris')

    def _swe_calc(self, datetime_utc):
        j = julday(datetime_utc)
        angles = [swe.calc_ut(j, i)[0] for i in range(Ephemeris.N_PLANETS)]
        return angles

    @classmethod
    def create(cls, datetime_utc):

        obj = cls()
        angles = obj._swe_calc(datetime_utc)
        for i, field in enumerate(obj._meta.fields[1:Ephemeris.N_PLANETS+1]):
            setattr(obj, field.name, angles[i])
        obj.save()
        return obj

    def __str__(self):
        return "Ephemeris <%d>" % self.pk

class Houses(models.Model):
    house_1 = models.FloatField()
    house_2 = models.FloatField()
    house_3 = models.FloatField()
    house_4 = models.FloatField()
    house_5 = models.FloatField()
    house_6 = models.FloatField()
    house_7 = models.FloatField()
    house_8 = models.FloatField()
    house_9 = models.FloatField()
    house_10 = models.FloatField()
    house_11 = models.FloatField()
    house_12 = models.FloatField()

    @classmethod
    def create(cls, datetime_utc, lat, lon):
        obj = cls()
        angles = obj._swe_calc(datetime_utc, lat, lon)
        for i, field in enumerate(obj._meta.fields[1:13]):
            setattr(obj, field.name, angles[i])
        obj.save()
        return obj

    def _swe_calc(self, datetime_utc, lat, lon):
        j = julday(datetime_utc)
        angles = swe.houses(j, lat, lon)[0]
        return angles

    def __str__(self):
        return "Houses <%d>" % self.pk




class Location(models.Model):
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    country = models.CharField(max_length=512)
    lat = models.FloatField()
    lng = models.FloatField()
    timezone = TimeZoneField()

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __unicode__(self):
        return "%s (%s)" % (self.city, self.country)

    def fill(self, g):
        self.city = g.city
        self.state = g.state
        self.country = g.country
        self.lat = g.lat
        self.lng = g.lng
        self.timezone = tzwhere.tzNameAt(self.lat, self.lng)


    @classmethod
    def create(cls, text):
        g = geocoder.google(text)
        if g.ok:
            objs = cls.objects.filter(city=g.city, state=g.state, country=g.country)
            if objs:
                obj = objs[0]
            else:
                obj = cls()
                obj.fill(g)
                obj.save()
            return obj
        return None