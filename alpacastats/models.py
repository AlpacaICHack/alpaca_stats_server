from __future__ import unicode_literals

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    date = models.DateField('date')
    picture = models.URLField()

    def __unicode__(self):
        return unicode(self.name)


class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    art = models.URLField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()

    event = models.ForeignKey(Event)

    active_track = models.BooleanField()

    timestamp = models.DateTimeField(auto_now=True)

    DJ = 'DJ'
    REQUEST = 'R'
    TRACK_TYPES = (
        (DJ, 'DJ\'s track'),
        (REQUEST, 'A request')
    )

    track_type = models.CharField(max_length=2, choices=TRACK_TYPES)

    def __unicode__(self):
        return unicode(self.name)


class Movement(models.Model):
    value = models.IntegerField()
    track = models.ForeignKey(Track)

    def __unicode__(self):
        return unicode(self.value)