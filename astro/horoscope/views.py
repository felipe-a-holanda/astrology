#coding: utf-8


import json
import urllib
import geocoder
import pytz
from datetime import datetime
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.utils import timezone
from .models import Ephemeris, Event, Houses, Location



from utils import PLANET_NAMES, SIGNS, dms


def test_anguglar(request):
    return render(request, 'horoscope/test_angular.html')

def home(request):
    now = timezone.now()
    params = {}
    params['datenow'] = now.strftime("%d/%m/%Y")
    params['timenow'] = now.strftime("%H:%M")

    return render(request, 'horoscope/home.html', params)

def my_events(request):

    return render(request, 'horoscope/event_list.html', {'events': Event.objects.all().select_related('ephemeris', 'location')})


def parse_date(date_str, time_str):
    now = datetime.now()
    if not date_str and not time_str:
        return now

    if not date_str:
        date = now.date()
    else:
        date = datetime.strptime(date_str, "%d-%m-%Y").date()

    if not time_str:
        time = now.time()
    else:
        time = datetime.strptime(time_str, "%H:%M").time()

    return datetime.combine(date, time)


def eph(request):
    data = {}
    date = request.GET.get('date', None)
    time = request.GET.get('time', None)

    date = parse_date(date, time)
    location = request.GET.get('city', None)

    if date and time and location:
        l = Location.create(location)
        date = l.timezone.localize(date)
        date = date.astimezone(pytz.utc)
        houses = Houses.create(date, l.lat, l.lng)
        data['houses'] = [getattr(houses, i.name) for i in houses._meta.fields[1:]]
        data['location'] = {'city': l.city, 'lat': dms(l.lat), 'lng': dms(l.lng)}

    data['planets'] = get_planets(date)
    data['date'] = str(date)


    return HttpResponse(
        json.dumps(data, indent=4),
        content_type='application/javascript; charset=utf8'
    )


def get_planets(date):
    e = Ephemeris.create(date)
    planets = []
    for index, field in enumerate(e._meta.fields[:11]):
        if field.name != 'id':
            v = getattr(e, field.name)
            planet = {}
            planet['index'] = index
            planet['name'] = field.name
            planet['angle'] = v
            planet['sign_index'] = int(v/30)
            planets.append(planet)
    return planets


def chart(request):
    date_str = request.GET.get('date', None)
    time_str = request.GET.get('time', None)
    date = parse_date(date_str, time_str)
    planets = []
    for p in get_planets(date):
        p['code'] = p['name']
        p['angle'] = p['angle'] % 30
        p['name'] = PLANET_NAMES[p['code']]
        p['sign_code'], p['sign']  = SIGNS[p['sign_index']]
        planets.append(p)

    return render(request, 'horoscope/chart.html', {'date': date, 'planets': planets})


def save_event(request):
    print 'save_event'
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')

        e = Event.create(name, date, time, location)
        e.save()
    print request.POST
    return HttpResponse(request.POST)

def geocode(request):
    query = request.GET.get('query', None)
    query = urllib.unquote(query).decode('utf8')
    g = geocoder.google(query)
    if g.ok and g.city:
        data = [{'value': g.address, 'tokens': g.city.split()}]
    else:
        data = {}

    data = json.dumps(data, cls=DjangoJSONEncoder, indent=2, separators=(',', ': '))

    return HttpResponse(data, content_type="application/json")

