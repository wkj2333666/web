from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db.models import Q
from SingerInfo.models import singer_info
from Search.models import search_song
import time
# Create your views here.

def singer_result(request, key_word, result=None, page_num=1, search_time=0, result_count=0):
    # singers = singer_info.objects.all()
    # if result is None:
    #     # the request is sent from web, instead of search() function!
    #     result = request.POST.get('result')
    
    real_page_num = page_num - 1
    page_size = settings.PAGE_SIZE
    ol_start_num = real_page_num * page_size + 1
    
    max_page_num = len(result) // page_size
    if (len(result) % page_size != 0):
        max_page_num += 1
    
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    template = loader.get_template("Search/singer.html")
    context = {
        "singers": result[real_page_num * page_size: page_num * page_size], 
        "root_url": settings.ROOT_URL,
        "page_size": page_size,
        "max_page_num": max_page_num,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "ol_start_num": ol_start_num,
        "result": result,
        "flag": 1,
        "key_word": key_word,
        "search_time": search_time,
        "result_count": result_count,
    }
    return HttpResponse(template.render(request=request, context=context))


def song_result(request, key_word, result=None, page_num=1, search_time=0, result_count=0):
    # if result is None:
        # the request is from web!
        # result = request.POST.get('result')

    page_size = settings.PAGE_SIZE
    max_page_num = len(result) // page_size
    if (len(result) % page_size != 0):
        max_page_num += 1
    
    real_page_num = page_num - 1
    ol_start_num = real_page_num * page_size + 1
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    template = loader.get_template("Search/song.html")
    context = {
        "songs": result[real_page_num * page_size: page_num * page_size],
        "root_url": settings.ROOT_URL,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "max_page_num": max_page_num,
        "ol_start_num": ol_start_num,
        "flag": 0,
        "key_word": key_word,
        "search_time": search_time,
        "result_count": result_count,
    }
    return HttpResponse(template.render(request=request, context=context))


def search(request):
    flag = int(request.POST.get('flag'))
    # 0 for song and 1 for singer
    key_word = request.POST.get('key_word')
    page_num = request.POST.get('page_num')
    if page_num is None:
        page_num = 1
    page_num = int(page_num)
    # template = loader.get_template("Search/result.html")

    result = None
    time_start = time.time()
    if flag == 0:
        result = search_song.objects.filter(
            Q(song_name__contains=key_word) |
            Q(singers_name__contains=key_word) |
            Q(lyric__contains=key_word)
        )

    else:
        result = singer_info.objects.filter(
            Q(singer_name__contains=key_word) |
            Q(singer_abstract__contains=key_word)
        )
    
    time_end = time.time()
    search_time = (time_end - time_start) * 1000 # ms
    result_count = len(result)
    return singer_result(request, key_word, result, page_num, search_time, result_count) \
        if flag else song_result(request, key_word, result, page_num, search_time, result_count)


def show_search_page(request):
    template = loader.get_template("Search/search.html")
    return HttpResponse(template.render(request=request, context=None))


# def goto_page(request):
#     goto_page = request.POST.get('goto_page')
#     flag = request.POST.get('flag')
#     return search(request, )