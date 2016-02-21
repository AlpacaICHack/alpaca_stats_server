from django import forms

class SearchForm(forms.Form):
    song_name = forms.CharField(label='Song name', max_length=100)
    artist_name = forms.CharField(label='Artist name', max_length=100)

class EventForm(forms.Form):
    event_title = forms.CharField(label='Event title', max_length=100)
    description = forms.CharField(label='Description', max_length=250)
    date = forms.DateField(label='Date')
    image_url = forms.CharField(label='Image URL', max_length=300)

