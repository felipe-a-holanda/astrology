from rest_framework import generics, permissions

from .serializers import EventSerializer, UserSerializer, EphemerisSerializer, EventInListSerializer
from horoscope.models import Event, Ephemeris
from profiles.models import UserProfile


class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    model = UserProfile
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class UserDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    model = UserProfile
    serializer_class = UserSerializer
    lookup_field = 'username'


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    model = Event
    serializer_class = EventInListSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    model = Event
    serializer_class = EventSerializer
    lookup_field = 'pk'
    permission_classes = [
        permissions.AllowAny
    ]



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
        return queryset.filter(user__username=self.kwargs.get('username'))

