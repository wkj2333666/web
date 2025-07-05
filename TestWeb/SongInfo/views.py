from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import song_info
from django.conf import settings
import datetime
# Create your views here.


def show_song_info(request, song_id, page_num):
    song = song_info.objects.get(song_id=song_id)
    
    page_size = settings.PAGE_SIZE
    max_page_num = len(song.comments) // page_size
    if (len(song.comments) % page_size != 0):
        max_page_num += 1
    
    real_page_num = page_num - 1
    # ol_start_num = real_page_num * page_size + 1
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    showed_song = song
    showed_song.comments = song.comments[
        real_page_num * page_size:
        page_num * page_size
    ]
    
    template = loader.get_template("SongInfo/song_info.html")
    context = {
        "song": showed_song,
        "root_url": settings.ROOT_URL,
        "org_url": settings.ORG_URL,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "max_page_num": max_page_num,
    }
    return HttpResponse(template.render(request=request, context=context))


def show_song_info_redirect(request, song_id):
    return HttpResponseRedirect(f"id={song_id}/page=1")


def show_song_list_redirect(request):
    return HttpResponseRedirect("list/page=1")


def show_song_list(request, page_num):
    songs = song_info.objects.all()
    
    page_size = settings.PAGE_SIZE
    max_page_num = len(songs) // page_size
    if (len(songs) % page_size != 0):
        max_page_num += 1
    
    real_page_num = page_num - 1
    ol_start_num = real_page_num * page_size + 1
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    template = loader.get_template("SongInfo/song_list.html")
    context = {
        "songs": songs[real_page_num * page_size: page_num * page_size],
        "root_url": settings.ROOT_URL,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "max_page_num": max_page_num,
        "ol_start_num": ol_start_num,
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
    # song.comments.append(new_comment)
    song.comments.insert(0, new_comment)

    song.full_clean()
    song.save()  # update_fields='comments')

    return HttpResponseRedirect(redirect_to=f"/song/id={song_id}/page=1")


def del_comment(request):
    song_id = request.GET.get("song_id")
    index = int(request.GET.get("index"))
    page = int(request.GET.get("page"))
    
    # 由于存在不同页，故传入的索引并非真实索引
    real_index = (page - 1) * settings.PAGE_SIZE + index

    song = song_info.objects.get(song_id=song_id)
    del song.comments[real_index]
    song.full_clean()
    song.save()

    return HttpResponseRedirect(redirect_to=f"/song/id={song_id}/page={page}")


def goto_page(request):
    goto_page = request.GET.get("goto_page")
    return HttpResponseRedirect(f"page={goto_page}")