from django.urls import path, include
import HomePage.views as views

urlpatterns = [path("", views.show_home)]
