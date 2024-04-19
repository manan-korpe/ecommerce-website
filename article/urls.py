from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path("articleList/",views.ShowArticleList,name='ShowArticleList'),
    path("showarticle/<int:article_id>",views.ShowArticle,name='showarticle'),
]