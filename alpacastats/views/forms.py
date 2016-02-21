from django import forms

class SongSearchForm(forms.Form):
    song_name = forms.CharField(label='Song name', max_length=100)
    artist_name = forms.CharField(label='Artist name', max_length=100)
