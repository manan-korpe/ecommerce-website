from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from .models import Article,Category
from store.models import *
# Create your views here.

def ShowArticleList(request):
    category = Category.objects.all()
    Article_list_data =  Article.objects.all()

    #pagenator for article
    paginator = Paginator(Article_list_data,6)
    page = request.GET.get('page')
    page_particle = paginator.get_page(page)

    data={
        'data':category,
        'articleld':page_particle,
    }
    return render(request,'article/article-list.html',data)

def ShowArticle(request,article_id):
    category = Category.objects.all()
    article_list_data = Article.objects.all()
    product_data = Product.objects.all()
    single_article=get_object_or_404(Article,pk=article_id)
    liked = []
    cart_product_list=[]

    if request.user.is_authenticated:
        cartId =Cart.objects.get(user=request.user)
        cart_list = Cart_item.objects.filter(cart=cartId)

        for cart in cart_list:
            cart_product_list.append(cart.product.id)

        like = LikedProduct.objects.filter(user=request.user)
        for like in like:
            liked.append(like.Product.id)
    else:
        cart_list = False
        liked = request.session.get('liked_products', [])

    data={
        'data':category,
        'like':liked,
        'articleld':article_list_data,
        'article':single_article,
        'product':product_data,
        'cart_product_list':cart_product_list
    }
    return render(request,'article/article-details.html',data)