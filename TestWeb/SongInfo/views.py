from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from .models import song_info
from django.conf import settings
# Create your views here.

def show_song_info(request, song_id):
    song = song_info.objects.get(song_id=song_id)
    template = loader.get_template('SongInfo/song_info.html')
    context = {
        'song': song,
        'root_url': settings.ROOT_URL,
    }
    return HttpResponse(template.render(request=request, context=context))
