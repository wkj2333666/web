from django.shortcuts import render
# from .models import song_list
from django.template import loader
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse


# Create your views here.
def show_home(request: HttpRequest):
    # songs = song_list.objects.all()
    template = loader.get_template("HomePage/home.html")
    # context = {"songs": songs}

    return HttpResponse(template.render(context=None, request=request))