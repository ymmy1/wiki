from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random")
]
