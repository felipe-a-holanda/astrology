from django.shortcuts import render

from rest_framework import serializers

from horoscope.models import Event, Location, Ephemeris
from profiles.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    #events = serializers.HyperlinkedIdentityField('events',  lookup_field='username')
    events = serializers.HyperlinkedIdentityField(view_name='userevent-list', lookup_field='username')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'events')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class EphemerisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ephemeris


class EventSerializer(serializers.ModelSerializer):

    location = LocationSerializer(read_only=True)
    #ephemeris = serializers.HyperlinkedIdentityField(view_name='ephemeris-detail', lookup_field='ephemeris')
    ephemeris = EphemerisSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'name', 'date', 'location', 'ephemeris')


class EventInListSerializer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='pk')

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'detail')
