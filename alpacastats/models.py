from __future__ import unicode_literals

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    picture = models.URLField()


class Track(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    art = models.URLField()
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()

    timestamp = models.DateTimeField(auto_now=True)

    DJ = 'DJ'
    REQUEST = 'R'
    TRACK_TYPES = (
        (DJ, 'DJ\'s track'),
        (REQUEST, 'A request')
    )

    track_type = models.CharField(max_length=2, choices=TRACK_TYPES)


class Movement(models.Model):
    value = models.IntegerField()
    track = models.ForeignKey(Track)