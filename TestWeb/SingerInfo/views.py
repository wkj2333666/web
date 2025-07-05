# %%
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import singer_info
from django.conf import settings


# Create your views here.
def show_singer_info(request, id, page_num=1):
    singer = singer_info.objects.get(singer_id=id)

    real_page_num = page_num - 1
    page_size = settings.PAGE_SIZE
    ol_start_num = real_page_num * page_size + 1
    
    max_page_num = len(singer.songs) // page_size
    if (len(singer.songs) % page_size != 0):
        max_page_num += 1
    
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    showed_singer = singer
    showed_singer.songs = singer.songs[
        real_page_num * page_size:
        page_num * page_size
    ]
    
    template = loader.get_template("SingerInfo/singer_info.html")
    context = {
        "singer": showed_singer,
        "img_path": f"singer_img/{singer.singer_id}.jpg",
        "root_url": settings.ROOT_URL,
        "org_url": settings.ORG_URL,
        "page_size": page_size,
        "max_page_num": max_page_num,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "ol_start_num": ol_start_num,
    }
    return HttpResponse(template.render(context, request))


def show_singer_info_redirect(request, id):
    return HttpResponseRedirect(f"id={id}/page=1")


def show_singer_list_redirect(request):
    return HttpResponseRedirect("list/page=1")

# %%
def show_singer_list(request, page_num=1):
    singers = singer_info.objects.all()
    
    real_page_num = page_num - 1
    page_size = settings.PAGE_SIZE
    ol_start_num = real_page_num * page_size + 1
    
    max_page_num = len(singers) // page_size
    if (len(singers) % page_size != 0):
        max_page_num += 1
    
    next_page = page_num + 1
    previous_page = page_num - 1
    if (next_page > max_page_num):
        next_page = max_page_num
    if (previous_page < 1):
        previous_page = 1
    
    template = loader.get_template("SingerInfo/singer_list.html")
    context = {
        "singers": singers[real_page_num * page_size: page_num * page_size], 
        "root_url": settings.ROOT_URL,
        "page_size": page_size,
        "max_page_num": max_page_num,
        "current_page": page_num,
        "next_page": next_page,
        "previous_page": previous_page,
        "ol_start_num": ol_start_num,
    }
    return HttpResponse(template.render(request=request, context=context))


def goto_page(request):
    goto_page = request.GET.get("goto_page")
    return HttpResponseRedirect(f"page={goto_page}")