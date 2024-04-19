"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from . import views,account
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
   
    path('admin/', admin.site.urls),
    #authentication
    path('signin/',account.sign_in,name='signin'),
    path('accounts/login/',account.user_login,name='login'),
    path('changepassword/',account.user_change_Passwordd,name='changepassword'),
    path('Forget-Password/',account.forget_password,name='forget_password'),
    path('forget-password-otpverify/',account.forget_password_otpverify,name="forget_password_otpverify"),
    path('forget-ResetPassword/',account.forget_ResetPassword,name="forget_ResetPassword"),
    path('logout/',account.user_logout,name='logout'),

    #cart
    path('articleApp/',include('article.urls'),name='articleList'),

    path('gardner/',include('gardner.urls'),name='gardner'),
    #store
    path('',views.home,name='home'),
    path('product/<int:product_id>',views.product,name='product'),
    
    path('productList/',views.productList,name='productList'),
    path('productList/<int:category_id>',views.productList,name='productList'),
    path('productList/<int:category_id>/<int:subcategory_id>',views.productList,name='productList'),

    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('get_cities/',views.get_cities),
    path('get_pin/',views.get_pin),
    path('orderDetail/<int:orderId>',views.orderDetails,name="order_details"),
    path('profile/',views.user_profile,name='profile'),

    #cart update,delete,add
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('update_cart/<int:product_id>',views.update_cart,name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>',views.remove_from_cart,name='remove_from_cart'),
    
    #profile view update,delete,add
    path('add_address/',views.add_address,name='add_address'),
    path('update_address/',views.update_address,name='update_address'),
    path('delete_address/<int:address_id>',views.delete_address,name="deleateaddress"),
    path('updateprofile/',views.update_profile,name='updateprofile'),    
    
    #ratting
    path('ratting/',views.ratting,name='ratting'),
    path('delete-ratting/<int:product>',views.delete_ratting,name="ratting"),

    #search url
    path('search/',views.search_product,name='search_product'),
   
   #like product url
    path('like/<int:product_id>',views.like,name='like'),   

    path('invoice/<int:orderid>',views.invoice,name="invoice"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

