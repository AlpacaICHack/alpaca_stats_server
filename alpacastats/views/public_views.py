import json
import urllib

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ..forms import SearchForm, EventForm
from ..models import Event, Track, Vote, Movement


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
    event = Event.objects.get(pk=event_id)

    context = {'event': event}


    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            search_track = ""
            first = True
            for s in str.split(str(form.cleaned_data['song_name'])):
                if first:
                    search_track += s
                    first = False
                else:
                    search_track += "+"
                    search_track += s

            search_artist = ""
            first = True
            for s in str.split(str(form.cleaned_data['artist_name'])):
                if first:
                   search_artist += s
                   first = False
                else:
                    search_artist += "+"
                    search_artist += s

            url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track=" + search_track + "&artist=" \
                  + search_artist + "&api_key=57ee3318536b23ee81d6b27e36997cde&format=json"

            response = urllib.urlopen(url)
            data = json.loads(response.read())

            art_url = data['results']['trackmatches']['track'][-1]['image'][3]['#text']
            name = data['results']['trackmatches']['track'][0]['name']
            artist = data['results']['trackmatches']['track'][0]['artist']

            track = Track()
            track.name = name
            track.artist = artist
            track.art = art_url
            track.track_type = 'DJ'
            track.active_track = False
            track.event = Event.objects.get(pk=event_id)
            track.played = False

            track.save()
            return HttpResponseRedirect(reverse('alpacastats:pool', args=[event_id]))
    else:
        return render(request, 'alpacastats/pool.html', context)




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


def event(request):
    #event = Event.objects.get(pk=event_id)

    #context = {'event': event}

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():

            event = Event()
            event.name = form.cleaned_data['event_title']
            event.date = form.cleaned_data['date']
            event.description = form.cleaned_data['description']
            event.picture = form.cleaned_data['image_url']

            event.save()
            return HttpResponseRedirect(reverse('alpacastats:pool', args=[event.id]))
    else:
        return render(request, 'alpacastats/new_event.html')
