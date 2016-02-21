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


def pool(request):
    pass


def statistics(request):
    pass