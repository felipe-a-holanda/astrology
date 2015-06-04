from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import EventSerializer, UserSerializer, EphemerisSerializer, EventInListSerializer, LocationSerializer
from horoscope.models import Event, Ephemeris, Location
from profiles.models import UserProfile





class LocationMixin(object):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class LocationList(LocationMixin, generics.ListCreateAPIView):
    pass


class LocationDetail(LocationMixin, generics.RetrieveAPIView):
    pass



class UserMixin(object):
    queryset = User.objects.all().select_related('profile')
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class UserList(UserMixin, generics.ListCreateAPIView):
    pass


class UserDetail(UserMixin, generics.RetrieveAPIView):
    pass


class EventMixin(object):
    queryset = Event.objects.all().select_related('ephemeris', 'location', 'houses')
    model = Event
    serializer_class = EventSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class EventList(EventMixin, generics.ListCreateAPIView):
    serializer_class = EventInListSerializer
    

class EventDetail(EventMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class EphemerisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ephemeris.objects.all()
    model = Ephemeris
    serializer_class = EphemerisSerializer
    permission_classes = [
        permissions.AllowAny
    ]



class UserEventList(generics.ListAPIView):
    queryset = Event.objects.all()
    model = Event
    serializer_class = EventInListSerializer

    def get_queryset(self):
        queryset = super(UserEventList, self).get_queryset()
        return queryset.filter(user=self.kwargs.get('pk'))

