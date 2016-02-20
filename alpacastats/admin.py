from alpacastats.models import Event, Track, Movement, Vote
from django.contrib import admin

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'picture')

class TrackAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'artist', 'art', 'active_track', 'track_type')

class MovementAdmin(admin.ModelAdmin):
    list_display = ('value', 'track')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'vote')

admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Movement, MovementAdmin)
admin.site.register(Vote, VoteAdmin)