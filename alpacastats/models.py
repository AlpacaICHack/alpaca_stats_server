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

    event = models.ForeignKey(Event)

    active_track = models.BooleanField()

    timestamp = models.DateTimeField(auto_now=True)

    played = models.BooleanField()

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

    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.value)

class Vote(models.Model):
    user = models.CharField(max_length=16)
    track = models.ForeignKey(Track)

    UPVOTE = 'U'
    DOWNVOTE = 'D'
    VOTE_TYPES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote')
    )

    vote = models.CharField(max_length=1, choices=VOTE_TYPES)

    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.user)