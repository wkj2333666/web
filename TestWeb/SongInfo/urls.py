"""
URL configuration for TestWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("id=<int:song_id>", views.show_song_info_redirect),
    path("id=<int:song_id>/page=<int:page_num>", views.show_song_info),
    path("id=<int:song_id>/goto", views.goto_page),
    path("list/page=<int:page_num>", views.show_song_list),
    path("list", views.show_song_list_redirect),
    path("list/goto", views.goto_page),
    path("comment/id=<int:song_id>", views.post_comment),
    path("del-comment", views.del_comment),
]
