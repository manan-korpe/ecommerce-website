from django.contrib import admin
from .models import Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id','title','related_category','image','create_at','update_on']
    list_editable=['related_category']
    list_display_links = ['image',]
    search_fields = ['title','related_category']

admin.site.register(Article,ArticleAdmin)