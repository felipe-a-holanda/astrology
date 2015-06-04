from django.core.management.base import BaseCommand
from horoscope.models import Event
from profiles.models import UserProfile
import csv


def create_event(row):
    print row
    username = row['username']
    name = row['name']
    date = row['date']
    time = row['time']
    location = row['local']
    u = UserProfile.objects.get(user__username=username)
    e = Event.create(name, date, time, location)
    e.user = u
    e.save()
    print "Event <%s> created" % e


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('events.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                create_event(row)
