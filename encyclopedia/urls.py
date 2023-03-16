from django.urls import path

from . import views
app_name = "entryName"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry , name="entry"),
    path("search",views.search ,name="search" ),
    path("newEntry",views.newEntry , name="newEntry"),
    path("wiki/<str:entry>/edit",views.edit , name= "edit"),
    path("random",views.randomPage,name="random")  
    
]
