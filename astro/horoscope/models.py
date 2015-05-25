#from datetime import datetime
from dateutil.parser import parse
import geocoder
import swisseph as swe
swe.set_ephe_path('/usr/share/libswe/ephe/')

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.db import models
from profiles.models import UserProfile


class Event(models.Model):
    user = models.ForeignKey(UserProfile, related_name='events', null=True)
    name = models.CharField(max_length=256)
    date = models.DateTimeField()
    location = models.ForeignKey('Location', related_name='events', null=True)
    ephemeris = models.ForeignKey('Ephemeris', related_name='event')

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return self.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    @classmethod
    def create(cls, name, date, time, location):
        datetime_utc = parse("%s %s" % (date, time))
        ephemeris = Ephemeris.create(datetime_utc)
        if ephemeris:
            ephemeris.save()
        else:
            print "error eph"

        location = Location.create(location)
        if location:
            location.save()
        else:
            print 'eror loc'

        self = cls()
        self.name = name
        self.date = datetime_utc
        self.ephemeris = ephemeris
        self.location = location
        return self




class Ephemeris(models.Model):
    NPLANETS = 23

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
        t = datetime_utc.timetuple()
        l = t[:3] + (t[3]+t[4]/60.0,)
        j = swe.julday(*l)
        angles = [swe.calc_ut(j, i)[0] for i in range(Ephemeris.NPLANETS)]

        for i, field in enumerate(self._meta.fields[1:Ephemeris.NPLANETS+1]):
            setattr(self, field.name, angles[i])

    @classmethod
    def create(cls, datetime_utc):
        obj = cls()
        obj._swe_calc(datetime_utc)
        return obj


class Location(models.Model):
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    country = models.CharField(max_length=512)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __unicode__(self):
        return "%s (%s)" % (self.city, self.country)

    def geocode(self, text):
        g = geocoder.google(text)
        if g.ok:
            print g
            from IPython import embed
            #embed()
            self.address = g.address
            self.city = g.city
            self.state = g.state
            self.country = g.country
            self.lat = g.lat
            self.lng = g.lng
        return g.ok

    @classmethod
    def create(cls, text):
        obj = cls()
        if obj.geocode(text):
            return obj
        else:
            return None

    def save(self, *args, **kwargs):
        if self.lat is None or self.lng is None:
            self.geocode(self.location)
        super(Location, self).save(*args, **kwargs)
