import json
from django.http import HttpResponse
from ..models import Event, Track, Movement


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

        track_vote_response = request.GET.get('up')

        if track_vote_response == 'true':
            track.upvotes += 1
        else:
            track.downvotes += 1

        track.save()

        return HttpResponse(json.dumps([track.name, track.upvotes, track.downvotes]), content_type=json)



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
    pass


def add_request(request):
    pass
