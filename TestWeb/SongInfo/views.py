from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import song_info
from django.conf import settings
import datetime
import json
# Create your views here.


def show_song_info(request, song_id):
    song = song_info.objects.get(song_id=song_id)
    template = loader.get_template("SongInfo/song_info.html")
    context = {
        "song": song,
        "root_url": settings.ROOT_URL,
        "org_url": settings.ORG_URL,
    }
    return HttpResponse(template.render(request=request, context=context))


def show_song_list(request):
    songs = song_info.objects.all()
    template = loader.get_template("SongInfo/song_list.html")
    context = {
        "songs": songs,
        "root_url": settings.ROOT_URL,
    }
    return HttpResponse(template.render(request=request, context=context))


def post_comment(request, song_id):
    data = request.POST
    user = data["user"]
    comment_content = data["content"]
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    new_comment = {
        "name": user,
        "content": comment_content,
        "time": date,
    }

    song = song_info.objects.get(song_id=song_id)
    # comments = json.loads(song.comments)
    song.comments.append(new_comment)
    # song.comments = json.dumps(comments)
    song.full_clean()
    song.save()  # update_fields='comments')

    return HttpResponseRedirect(redirect_to=f"/song/id={song_id}")


def del_comment(request):
    song_id = request.GET.get("song_id")
    index = int(request.GET.get("index"))

    song = song_info.objects.get(song_id=song_id)
    del song.comments[index]
    song.full_clean()
    song.save()

    return HttpResponseRedirect(redirect_to=f"/song/id={song_id}")
