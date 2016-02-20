import json
from django.http import HttpResponse
from django.shortcuts import render
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
    pass


def vote_track(request):
    pass


def vote_request(request):
    pass


def movement(request):
    pass


def vote(request):
    pass


def add_request(request):
    pass
