from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import serializers

from horoscope.models import Event, Location, Ephemeris, Houses, Location
from profiles.models import UserProfile


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location


class UserProfileSerializer(serializers.ModelSerializer):
    events = serializers.HyperlinkedIdentityField(view_name='user-event-list')
    detail = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = UserProfile
        fields = ('name', 'detail', 'events')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')

    def create(self, data):
        return User.objects.create(**data)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class EphemerisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ephemeris


class HousesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Houses


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    #user = UserSerializer()
    location = LocationSerializer(read_only=True)
    ephemeris = EphemerisSerializer(read_only=True)
    houses = HousesSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'user', 'name', 'date', 'city', 'location', 'ephemeris', 'houses')


class EventInListSerializer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='pk')

    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'city', 'detail')
