from django.shortcuts import render
from .models import SongList
from django.template import loader
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse

# Create your views here.
def show_song(request: HttpRequest):
    songs = SongList.objects.all()
    template = loader.get_template('HomePage/home.html')
    context = {
        'songs': songs
    }
    
    return HttpResponse(template.render(context=context, request=request))