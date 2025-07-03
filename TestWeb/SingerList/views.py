from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from SingerInfo.models import singer_info
from django.conf import settings

# Create your views here.
def show_singer_list(request):
    singers = singer_info.objects.all()
    template = loader.get_template('SingerList/singer_list.html')
    context = {
        'singers': singers,
        'root_url': settings.ROOT_URL
    }
    return HttpResponse(template.render(request=request, context=context))