from django.shortcuts import render

from rest_framework import serializers

from horoscope.models import Event, Location, Ephemeris
from profiles.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    events = serializers.HyperlinkedIdentityField(view_name='user-event-list')
    detail = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'detail', 'events')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class EphemerisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ephemeris


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='user-event-list')
    location = LocationSerializer(read_only=True)
    ephemeris = EphemerisSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'name', 'date', 'location', 'ephemeris')


class EventInListSerializer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='pk')

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'detail')
