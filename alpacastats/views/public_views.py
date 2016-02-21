import json
import urllib

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from ..forms import SearchForm
from ..models import Event, Track


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

            track.save()
            return HttpResponseRedirect(reverse('alpacastats:pool', args=[event_id]))
    else:
        return render(request, 'alpacastats/pools.html', context)


def statistics(request, event_id):
    event = Event.objects.get(pk=event_id)

    activetracks = Track.objects.filter(event__pk=event.pk).filter(active_track=True)
    if len(activetracks) > 0:
        currenttrack = activetracks[0]
    else:
        currenttrack = None

    context = {'currenttrack': currenttrack, 'event': event}

    return render(request, 'alpacastats/stats.html', context)