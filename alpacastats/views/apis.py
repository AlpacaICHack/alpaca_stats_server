import urllib, json

import datetime

from django.http import HttpResponse
from django.utils import timezone
from ..models import Event, Track, Movement, Vote


def events(request):
    event_id_response = request.GET.get('id')
    response_data = []
    events = []

    if not event_id_response is None:
        event_id = int(event_id_response)
        try:
            events.append(Event.objects.get(pk=event_id))
        except Event.DoesNotExist:
            pass

    else:
        events = Event.objects.all()

    for e in events:
        eventdata = {}
        eventdata['id'] = e.pk
        eventdata['name'] = e.name
        eventdata['description'] = e.description
        eventdata['date'] = e.date.strftime("%a, %d %b %Y")
        eventdata['picture'] = e.picture
        response_data.append(eventdata)

    out = json.dumps(response_data)

    return HttpResponse(out, content_type=json)


def pool(request):
    event_id_response = request.GET.get('event')
    tracks_data = []

    if event_id_response is None:
        return HttpResponse("Please supply an event ID!", content_type=json)
    else:
        event_id = int(event_id_response)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event doesn't exist", content_type=json)

        tracks = Track.objects.filter(event__pk=event.pk)

        for t in tracks:
            track = {}
            track['id'] = t.pk
            track['name'] = t.name
            track['artist'] = t.artist
            track['artwork'] = t.art
            if t.track_type == 'DJ':
                track['request'] = False
            else:
                track['request'] = True

            tracks_data.append(track)

        tracks_out = json.dumps(tracks_data)

        return HttpResponse(tracks_out, content_type=json)


def current_track(request):
    event_id_response = request.GET.get('event')
    tracks_data = []

    if event_id_response is None:
        return HttpResponse("Please supply an event ID!", content_type=json)
    else:
        event_id = int(event_id_response)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event doesn't exist", content_type=json)

        t = Track.objects.filter(event__pk=event.pk).filter(active_track=True)[0]

        track = {}
        track['id'] = t.pk
        track['name'] = t.name
        track['artist'] = t.artist
        track['artwork'] = t.art
        if t.track_type == 'DJ':
            track['request'] = False
        else:
            track['request'] = True

        track_out = json.dumps(track)

        return HttpResponse(track_out, content_type=json)


def vote_track(request):
    track_id_response = request.GET.get('track')
    tracks_data = []

    if track_id_response is None:
        return HttpResponse("Please supply a track ID!", content_type=json)
    else:
        track_id = int(track_id_response)

        try:
            track = Track.objects.get(pk=track_id)
        except Event.DoesNotExist:
            return HttpResponse("Track doesn't exist", content_type=json)

        track = Track.objects.get(pk=track_id)
        user = request.GET.get('user')

        if user is not None:
            v = Vote()
            v.user = str(user)
            v.track = track
            vote_result = request.GET.get('up')
            if vote_result is not None:
                if vote_result == 'true':
                    v.vote = 'U'
                else:
                    v.vote = 'D'

                v.save()
                return HttpResponse(json.dumps([v.user, v.track.name]), content_type=json)
            return HttpResponse("No vote type specified!", content_type=json)
        else:
            return HttpResponse("No user ID specified!", content_type=json)


def movement(request):
    event_id_response = request.GET.get('event')

    if event_id_response is None:
        return HttpResponse("Please supply an event ID!", content_type=json)
    else:
        event_id = int(event_id_response)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event doesn't exist", content_type=json)

        active_track = Track.objects.filter(event__pk=event.pk).filter(active_track=True)[0]

        if request.GET.get('value') is not None:
            m = Movement()
            m.value = request.GET.get('value')
            m.track = active_track
            m.save()
            return HttpResponse(json.dumps([m.value, m.track.name]), content_type=json)
        else:
            return HttpResponse("Please supply a movement value!", content_type=json)


def vote(request):
    event_id_response = request.GET.get('event')

    if event_id_response is None:
        return HttpResponse("Please supply an event ID!", content_type=json)
    else:
        event_id = int(event_id_response)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return HttpResponse("Event doesn't exist", content_type=json)

        t = Track.objects.filter(event__pk=event.pk).filter(active_track=True)[0]

        user_response = request.GET.get('user')

        if user_response is not None:
            trackvotes = Vote.objects.filter(track__pk=t.pk)
            hasvote = False
            thisvote = Vote()
            user = str(user_response)
            for v in trackvotes:
                if v.user == user:
                    hasvote = True
                    thisvote = v

            if not hasvote:
                thisvote.user = str(user)
                thisvote.track = t

            vote_result = request.GET.get('up')
            if vote_result is not None:
                if vote_result == 'true':
                    thisvote.vote = 'U'
                else:
                    thisvote.vote = 'D'

                thisvote.save()
                return HttpResponse(json.dumps([thisvote.user, thisvote.track.name]), content_type=json)
            return HttpResponse("No vote type specified!", content_type=json)
        else:
            return HttpResponse("No user ID specified!", content_type=json)


def add_request(request):
    event_id_response = request.GET.get('event')
    track_name_response = request.GET.get('track')
    artist_name_response = request.GET.get('artist')

    if event_id_response is not None and track_name_response is not None and artist_name_response is not None:
        event_id = int(event_id_response)
        track_name = str(track_name_response)
        artist_name = str(artist_name_response)

        search_track = ""
        first = True
        for s in str.split(track_name):
            if first:
                search_track += s
                first = False
            else:
                search_track += "+"
                search_track += s

        search_artist = ""
        first = True
        for s in str.split(artist_name):
            if first:
                search_artist += s
                first = False
            else:
                search_artist += "+"
                search_artist += s

        url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track=" + search_track + "&artist=" +\
              search_artist + "&api_key=57ee3318536b23ee81d6b27e36997cde&format=json"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        print url

        art_url = data['results']['trackmatches']['track'][-1]['image'][3]['#text']
        name = data['results']['trackmatches']['track'][0]['name']
        artist = data['results']['trackmatches']['track'][0]['artist']

        track = Track()
        track.name = name
        track.artist = artist
        track.art = art_url
        track.track_type = 'R'
        track.active_track = False
        track.event = Event.objects.get(pk=event_id)

        track.save()

    return HttpResponse(json.dumps([track.name, track.artist, track.art]), content_type=json)


def movement_data(request):
    event_id_response = request.GET.get('event')

    if event_id_response is not None:
        event = Event.objects.get(pk=int(event_id_response))

        tracks = Track.objects.filter(event__pk=event.pk).filter(active_track=True)

        if len(tracks) > 0:
            track = tracks[0]

            moves = Movement.objects.filter(track__pk=track.pk).order_by('-timestamp').filter(timestamp__gt=timezone.now() - datetime.timedelta(0, 2))

            print timezone.now() + datetime.timedelta(0, 60)

            movesum = 0

            for m in moves:
                print m.timestamp
                movesum += m.value

            outsum = json.dumps({'movement': movesum})

            return HttpResponse(outsum, content_type=json)

def votes_data(request):
    event_id_response = request.GET.get('event')

    if event_id_response is not None:
        event = Event.objects.get(pk=int(event_id_response))

        tracks = Track.objects.filter(event__pk=event.pk).filter(active_track=True)

        if len(tracks) > 0:
            track = tracks[0]

            upvotes = Vote.objects.filter(track__pk=track.pk).filter(vote='U').count()
            downvotes = Vote.objects.filter(track__pk=track.pk).filter(vote='D').count()

            outvotes = json.dumps({'upvotes': upvotes, 'downvotes': downvotes})

            return HttpResponse(outvotes, content_type=json)


