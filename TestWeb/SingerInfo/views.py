# %%
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import singer_info
from django.conf import settings


# Create your views here.
def show_singer_info(request, id):
    singer = singer_info.objects.get(singer_id=id)
    template = loader.get_template('SingerInfo/singer_info.html')
    context = {
        'singer': singer,
        'img_path': f'singer_img/{singer.singer_id}.jpg',
        'root_url': settings.ROOT_URL,
        'org_url': settings.ORG_URL,
    }
    return HttpResponse(template.render(context, request))
# %%
def show_singer_list(request):
    singers = singer_info.objects.all()
    template = loader.get_template('SingerInfo/singer_list.html')
    context = {
        'singers': singers,
        'root_url': settings.ROOT_URL
    }
    return HttpResponse(template.render(request=request, context=context))