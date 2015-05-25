from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')

admin.site.register(Event, EventAdmin)
admin.site.register(Ephemeris)
admin.site.register(Location)