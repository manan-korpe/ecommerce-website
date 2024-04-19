from django.db import models
from store.models import *
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/img/Article/")
    body = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    related_category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True, null=True)