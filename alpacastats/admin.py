from alpacastats.models import Event, Track, Movement
from django.contrib import admin

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'picture')

class TrackAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'artist', 'art', 'upvotes', 'downvotes', 'active_track', 'track_type')

class MovementAdmin(admin.ModelAdmin):
    list_display = ('value', 'track')

admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Movement, MovementAdmin)