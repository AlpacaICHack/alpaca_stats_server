import json
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Event, Track, Movement


def events(request):
    event_id_response = request.GET.get('id')
    response_data = []
    if event_id_response == "":
        event_id = int(event_id_response)
        Event.objects.get(event_id)
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
