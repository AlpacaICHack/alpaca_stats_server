from django.http import HttpResponse
from django.shortcuts import render
from ..models import Event, Track, Movement, Vote

# Create your views here.

def home(request):
    events = Event.objects.all().order_by('-date')

    currenttracks = []
    for e in events:
        if len(Track.objects.filter(event__pk=e.pk).filter(active_track=True)) > 0:
            currenttrack = Track.objects.filter(event__pk=e.pk).filter(active_track=True)[0]
        else:
            currenttrack = None
        currenttracks.append(currenttrack)

    context = {'events': zip(events, currenttracks)}
    return render(request, 'alpacastats/home.html', context)


def pool(request, event_id):
    return render(request, 'alpacastats/pools.html')


def statistics(request, event_id):

    event = Event.objects.get(pk=event_id)

    track_id_response = request.GET.get('track_id')
    if track_id_response is not None:
        newactive = Track.objects.get(pk=int(track_id_response))
        activetracks = Track.objects.filter(event__pk=event.pk).filter(active_track=True)
        if len(activetracks) > 0:
            for t in activetracks:
                t.active_track = False
                t.played = True
                t.save()

        newactive.active_track = True
        newactive.save()

    alltracks = Track.objects.filter(event__pk=event.pk)
    votes = []

    for t in alltracks:
        up = Vote.objects.filter(track__pk=t.pk).filter(vote='U').count()
        down = Vote.objects.filter(track__pk=t.pk).filter(vote='D').count()
        votes.append({'up': up, 'down': down})

    activetracks = Track.objects.filter(event__pk=event.pk).filter(active_track=True)
    if len(activetracks) > 0:
        currenttrack = activetracks[0]
    else:
        currenttrack = None



    context = {'currenttrack': currenttrack, 'event': event, 'tracks': zip(alltracks, votes)}

    return render(request, 'alpacastats/stats.html', context)