from django.contrib import admin
from django.urls import path
from gardner import views
from django.conf import settings

urlpatterns =[
    path("",views.gardnerlist,name="gardnerlist"),
    path("booking/<int:gardnerid>",views.booking,name="booking"),
    path("dateslot/",views.dateslot,name="dateslot"),
]