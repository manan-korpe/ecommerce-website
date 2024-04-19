from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import sign_in_form
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives,send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from store.models import *
from article.models import *
from gardner.models import *
from .forms import Custuserform,ShippingForms,Forget_Password_Form,OtpVerify_Form,Forget_new_password_Form,ProfilePictureForm
import random,string
from datetime import datetime
import json
import razorpay

#invoice
from django.template.loader import get_template
from xhtml2pdf import pisa
client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_SECRET))


def invoice(request, orderid):
    # Fetch the order and related order items
    order = Order.objects.get(pk=orderid)
    order_items = OrderItem.objects.filter(order=order)

    # Prepare context for the template
    context = {
        "order": order,
        "items": order_items,  # Renamed to items for clarity
    }

    # Render the invoice HTML template
    template = get_template('email/invoice.html')  # Adjust the path as needed
    html = template.render(context)

    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{orderid}_invoice.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(
        html, dest=response,
        encoding='utf-8'
    )

    # If error during PDF creation
    if pisa_status.err:
        return HttpResponse('We had some errors during PDF generation')

    return response

def homedemo(request):
    return render(request,"./demo/login.html")

def home(request):
    Category_list= Category.objects.all()
    sub_category = SubCategory.objects.all()
    product = Product.objects.all()
    article_list = Article.objects.all()
    cart_product_list = []
    liked=[]
            
    new_product = Product.objects.order_by("-create_at")
    #Retriev liked  or not liked data form login or nont login user
    
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
        'new_product':new_product,
        'product':product,
        'data':Category_list,
        'subcateogry':sub_category,
        'article':article_list,
        'like':liked,
        'cart_product_list':cart_product_list,
    }
    return render(request,'store/index.html',data)

def productList(request,category_id=None,subcategory_id=None):
    data = Category.objects.all()
    cart_product_list=[]
    
    #Retriev liked  or not liked data form login or nont login user
    liked=[]

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
        
    if category_id != None and subcategory_id == None:
        category=  SubCategory.objects.filter(category=category_id)
        product_list = Product.objects.filter(category__in=category)
    elif category_id != None and subcategory_id != None:
        category= get_object_or_404(SubCategory,pk=subcategory_id)
        product_list = Product.objects.filter(category=category)
    else:
        product_list = Product.objects.all()
        
    sort_option = request.GET.get('sort')
    if sort_option == 'price':
        product_list = product_list.order_by('offer_price')
    elif sort_option == 'pricedes':
        product_list = product_list.order_by('-offer_price')
    elif sort_option == 'name':
        product_list = product_list.order_by('title')
    elif sort_option == 'nameZtoA':
        product_list = product_list.order_by('-title')
        
    #pagenator for products
    paginator = Paginator(product_list,16)
    page = request.GET.get('page')
    page_product = paginator.get_page(page)
    product_count = product_list.count()
    
    context={
        'data':data,
        'cart_list':cart_list,
        'cart_product_list':cart_product_list,
        'product':page_product,
        'like':liked,
    }
    
    return render(request,'store/product-list.html',context)

def product(request,product_id):
    data = Category.objects.all()
    singleProduct= get_object_or_404(Product,pk=product_id)
    images = ProductImage.objects.filter(Product=singleProduct)
    print(images)
    specifications = ProductDetails.objects.get(product=product_id)
    caretips = CareTips.objects.get(product=product_id)
    rated = Review.objects.filter(product=singleProduct)
    cart_product_list = []
    liked=[]

    #singleProduct details store in dis
    field_values = {}
    for field in specifications._meta.get_fields():
        if not (field.primary_key or field.is_relation):
            verbose_name = field.verbose_name
            field_value = getattr(specifications, field.name)
            if field_value is not None:
                field_values[verbose_name] = field_value

    #care tips details store in dis
    care = {}
    for field in caretips._meta.get_fields():
        if not (field.primary_key or field.is_relation):
            verbose_name = field.verbose_name
            field_value = getattr(caretips, field.name)
            if field_value is not None:
                care[verbose_name] = field_value

    
    
    related_product_list = Product.objects.filter(category=singleProduct.category)
    related_product_list =related_product_list.exclude(id=product_id)
    
    cart_product = False
    status = False
    
            
    #Retriev liked  or not liked data form login or nont login user
    
    if request.user.is_authenticated:
        orderID = Order.objects.filter(user=request.user)
        order_items = OrderItem.objects.filter(order__in=orderID)

        for order_item in order_items:
            if(order_item.order.status == 'delivered'):
                if product_id == order_item.product.pk:
                    status = True
                    for rated_item in rated:
                        if rated_item.user == request.user:
                            status = False

        try:
            cart = Cart.objects.get(user=request.user)
            cart_product = Cart_item.objects.get(cart=cart,product=product_id)
        except Cart_item.DoesNotExist:
            cart_product = False
            
        cartId =Cart.objects.get(user=request.user)
        cart_list = Cart_item.objects.filter(cart=cartId)

        for cart in cart_list:
            cart_product_list.append(cart.product.id)

        like = LikedProduct.objects.filter(user=request.user)
        for l in like:
            liked.append(l.Product.id)
        user = Customeruser.objects.get(user=request.user)
        review = Review.objects.filter(product=product_id,user=user).first()
    else:
        cart_list = False
        liked = request.session.get('liked_products', [])
        review = False
    

    context={
        'product':singleProduct,
        'images':images,
        'like':liked,
        'specifications':field_values,
        'status':status,
        'rated':rated,
        'care':care,
        'data':data,
        'review':review,
        'related_product_list':related_product_list,
        'cart_product_list':cart_product_list,
        'cart_product':cart_product
    }
    return render(request,'store/product.html',context)

def aboutUs(request):
    data = Category.objects.all()
    return render(request, 'store/about-us.html', {'data': data})

def contact(request):
    data = Category.objects.all()
    return render(request, 'store/contact.html', {'data': data})

@login_required
def user_profile(request): 
    if request.method == 'POST':
        profile_pic = Customeruser.objects.get(user=request.user)
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile_pic)
        if form.is_valid():
            img = form.cleaned_data['user_image']
            instance = form.save(commit=False)
            print("Before save:", instance.user_image)  # Print the image field before saving
            instance.save()
            print("After save:", instance.user_image)
            return redirect('store/profile')  # Redirect to profile page after successful upload
         
    else:  
        order = Order.objects.filter(user=request.user).order_by('-created_at') 
        pay = Payment.objects.all()
        payment =[]
        for item in pay:
            if item.order.user == request.user :
                payment.append(item)
            
        booking = Booking.objects.filter(customer=request.user).order_by('-created')        
        try:
            fulladdress = ShippingAddress.objects.get(user=request.user)
            address_form = ShippingForms(instance=fulladdress)
            profile_pic = Customeruser.objects.get(user=request.user)
            profile_form = ProfilePictureForm(instance=profile_pic)
        except ShippingAddress.DoesNotExist:
            fulladdress = None
            address_form = ShippingForms()
            profile_form = ProfilePictureForm()
        
        Category_data= Category.objects.all()
        personal_custuser_value,create = Customeruser.objects.get_or_create(user=request.user)
    
        user_details_form = Custuserform(initial={
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'phone_one':personal_custuser_value.phone_one,
            'phone_second':personal_custuser_value.phone_second,
        })

        data={
            'data':Category_data,
            'order':order,
            'payment':payment,
            "booking":booking,
            'name':request.user.username,
            'address':fulladdress,
            'custform':user_details_form,
            'address_form':address_form,
            'profile_form':profile_form,
            'custuser':personal_custuser_value
        }
    return render(request,'store/profile.html',data)

@login_required
def add_address(request):
    if request.method == 'POST':
        form = ShippingForms(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request,"Address added successfully")
            return redirect('profile')
        else:
            print("form invaild")
            messages.error(request,form.errors)
            return redirect('profile')

@login_required
def update_address(request):
    Address = ShippingAddress.objects.get(user=request.user)
    if request.method == 'POST':
        form = ShippingForms(request.POST , instance=Address)
        if form.is_valid():
            form.save()
            messages.success(request,"Address updated successfully")
            return redirect('profile')
        else:
            messages.error(request,"address not updated......!")
               
            return redirect('profile',phone_one=request.POST.get('phone_one'))

@login_required
def delete_address(request,address_id):
    try:
        Address =ShippingAddress.objects.get(pk=address_id)
        Address.delete()
        return JsonResponse({'messages':'address deleted successfully'})
    except ShippingAddress.DoesNotExist:
        return JsonResponse({'error':'address not deleted'})

@login_required
def update_profile(request):
    custuser= Customeruser.objects.get(user=request.user) 
    if request.method == 'POST':
        custform = Custuserform(request.POST)
        
        if custform.is_valid():
            request.user.first_name = custform.cleaned_data['first_name']
            request.user.last_name = custform.cleaned_data['last_name']
            request.user.email = custform.cleaned_data['email']
            custuser.phone_one = custform.cleaned_data['phone_one']
            custuser.phone_second = custform.cleaned_data['phone_second']
            
            if request.user.email:
                if User.objects.filter(email=request.user.email).exclude(pk=request.user.pk).exists():
                    messages.error(request,"your new email id already in user Enter another email id ")
                    return redirect('profile')
                
            custuser.save()
            request.user.save()
            messages.success(request,"profile updated successfully")
            return redirect('profile')
        else:
            messages.error(request,"Enter correct profile details   ")
            return redirect('profile')

@login_required
def cart(request):      
    data = Category.objects.all()
    cart_details,create = Cart.objects.get_or_create(user=request.user)
    cart_item = Cart_item.objects.filter(cart=cart_details.pk)
    shipping_address= ShippingAddress.objects.filter(user=request.user)

    shipping_crg=0
    discount = 0
    
    #discount calculate
    for item in cart_item:
        dis = (item.product.price-item.product.offer_price)*item.quantity
        discount += dis

    #shipping charges
    for item in cart_item:
        if item.product.shipping_charges > shipping_crg:
            shipping_crg += item.product.shipping_charges

    if cart_details.total_cart>=1000 or cart_details.total_cart==0:
        shipping_crg = 0


    total = cart_details.total_cart+shipping_crg

    request.session['shipping_charge'] = float(shipping_crg)
    request.session['discount'] = float(discount)
    request.session['total'] = float(total)

    

    context={
        'data':data,
        'cart_details':cart_details,
        'cart_item':cart_item,
        'address':shipping_address,
        'shipping_charge':shipping_crg,
        'total':total,
        'discount':discount
    }
    return render(request,'store/cart.html',context)

@login_required   
def add_cart(request,product_id):
    print('called')
    product=Product.objects.get(pk=product_id)
    cart_id = Cart.objects.get(user=request.user)
    cart_item, created = Cart_item.objects.get_or_create(cart=cart_id, product=product)
    
    if product.quantity == 0:
        return JsonResponse({'success':False,'message':'product out of stock'})
    else:
        if created:
            cart_item.quantity =1
            cart_item.save()
            return JsonResponse({'success':'True','message':'product added to cart successfuly'})
        else:
            return JsonResponse({'success':False,'message':'product already in cart'})

@login_required          
def update_cart(request,product_id):
    product=Product.objects.get(pk=product_id)
    cart_id = Cart.objects.get(user=request.user)
    cart_item = Cart_item.objects.get(cart=cart_id, product=product)
    quantity = int(request.POST.get('qty'))
    
    
    if product.quantity == 0:
        return JsonResponse({'success':False,'message':'product out of stock'})
    else:
        if quantity <=0:
            cart_item.delete()
            return JsonResponse({'success':False,'message':'your quntity is zero'})
        else:
            if quantity <= product.quantity:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({'success':True,'message':'product added to cart successfuly'})
            else:
                print('false')
                return JsonResponse({'success':False,'message':'your quntity are more then curret stock'})

@login_required
def remove_from_cart(request,cart_item_id):
    cart_id= Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(Cart_item,pk=cart_item_id,cart=cart_id)
    cart_item.delete()

    return redirect('cart')

@csrf_exempt
def checkout(request):
    if request.method == 'POST':        
        custData = Customeruser.objects.get(user=request.user)
        cartId = Cart.objects.get(user=request.user)
        cart_item = Cart_item.objects.filter(cart=cartId)


        #shipping addres data
        shipping_status = request.POST.get('shipping-value')#give shipping address is new or old
        print(shipping_status)
        if shipping_status == 'new':
            sfname = request.POST.get('fname')
            slname = request.POST.get('lname')
            sphone = request.POST.get('phone')
            saddress = request.POST.get('address')
            slandmark = request.POST.get('landmark')
            sstate = request.POST.get('state')
            scity = request.POST.get('city')
            spin_code = request.POST.get('pin_code')
            print(sfname,slname,sphone,saddress,slandmark,scity,spin_code)
        else:
            try:
                defultAddress = ShippingAddress.objects.get(user=request.user)

                sfname = request.user.first_name
                slname = request.user.last_name
                sphone =  defultAddress.phone
                saddress = defultAddress.address
                slandmark = defultAddress.landmark
                sstate = defultAddress.state
                scity = defultAddress.city
                spin_code = defultAddress.pin_code
                print(sfname,slname,sphone,saddress,slandmark,scity,spin_code)
            except:
                print("address not fount ")
        
        bill_status = request.POST.get('bill-address')#give billing address is new or same as shipping address
        print(bill_status)

        if bill_status == 'same':
            bfname = sfname
            blname = slname
            bphone = sphone
            baddress = saddress
            blandmark = slandmark
            bstate = sstate
            bcity = scity
            bpin_code = spin_code
            print(bfname,blname,bphone,baddress,blandmark,bcity,bpin_code)
        else:
            bfname = request.POST.get('bfname')
            blname = request.POST.get('blname')
            bphone = request.POST.get('bphone')
            baddress = request.POST.get('baddress')
            blandmark = request.POST.get('blandmark')
            bstate = request.POST.get('bstate')
            bcity = request.POST.get('bcity')
            bpin_code = request.POST.get('bpin_code')
            print(bfname,blname,bphone,baddress,blandmark,bcity,bpin_code)

        payment = request.POST.get('pay')
        status_val = "pending"
        payment_stat = " "
        order_shipping_charge = request.session.get('shipping_charge', '0.00')
        order_discount = request.session.get('discount', '0.00')
        order_total = request.session.get('total', '0.00')

        pay_id = " "
        
        '''-------------------------------
        '''
        if payment == "Razorpay":
            payment_stat = "Confirm"
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            try:
                # Assuming client is already defined
                check_signature = client.utility.verify_payment_signature(params_dict)
                pay_id = razorpay_payment_id
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        elif payment == 'COD':
                payment_stat = "pending"   
        else:
            messages.error(request, "Failed to order.")
            return redirect('checkout')
        
        print(scity)
        print(sstate)
        print(spin_code)
        order = Order(
            user=request.user,
            fname=sfname, lname=slname, phone=sphone, address=saddress, landmark=slandmark, city=scity,
            state=sstate, pin_code=spin_code, amount=cartId.total_cart, discount=order_discount,
            shipping_charges=order_shipping_charge, total_amount=order_total,
            status=status_val, update_at=datetime.now()
        )
        
        order.save()
        
        pay = Payment(order=order,payment_method=payment,payment_id=pay_id,amount=order_total,status=payment_stat,updated_at=datetime.now())
        pay.save()

        # Save order items
        for item in cart_item:
            order_item = OrderItem(
                order=order, product=item.product, quantity=item.quantity, price=item.product.price,discount_price=item.product.offer_price
                ,subtotal=item.discount_price, update_at=datetime.now()
            )
            order_item.save()
            # Update product quantity
            pqty = Product.objects.get(pk=item.product.id)
            pqty.quantity = pqty.quantity - item.quantity
            pqty.save()

            # Delete cart item
            item.delete()

        # Save order bill
        bill = OrderBill(
            order=order, fname=bfname, lname=blname, phone=bphone, address=baddress, landmark=blandmark,
            city=bcity, state=bstate, pin_code=bpin_code
        )
        bill.save()
        order_id = order.id
        
        #email sending logic----------------------------------------------
        uemail= request.user.email        
        orderlist = OrderItem.objects.filter(order=order)
        context={
            "order":order,
            "orderlist":orderlist,
        }
        
        html_message = render_to_string('template/Email/order_confirm.html',context)
        plain_email = strip_tags(html_message)
        message = EmailMultiAlternatives(
            subject='Order confirmation',
            body=plain_email,
            from_email=settings.EMAIL_HOST_USER,
            to=[uemail]
        )
        message.attach_alternative(html_message,'text/html')
        message.send()
        #close email sending logic----------------------------------------------

        messages.success(request,"your order confirem successfully..")
        return redirect("order_details",orderId=order_id)
    else:
        data = Category.objects.all()
        city = City.objects.all()
        state = State.objects.all()
        pincode = Pin_Code.objects.all()

        shipping_address = ShippingAddress.objects.filter(user=request.user)
        user = Customeruser.objects.get(user=request.user)
        
        cart_user = Cart.objects.get(user=request.user)
        product = Cart_item.objects.filter(cart=cart_user)
        if product.exists():
            #get charges store in session
            shipping_charge = request.session.get('shipping_charge', '0.00')
            discount = request.session.get('discount', '0.00')
            total = request.session.get('total', '0.00')
        else:
            messages.error(request,"Yor cart is empty thats why you dont check out")
            return redirect('cart')

        #razorpay code online payment
        order = client.order.create(dict(amount=total*100,currency="INR"))
    
        context={
            'data':data,
            'city':city,
            'state':state,
            'pincode':pincode,
            'shipping_address':shipping_address,
            'user':user,
            'cart':product,
            'cart_user':cart_user,
            'shipping_charge':shipping_charge,
            'discount':discount,
            'total':total,
            'order_id':order["id"],
            'amount':order["amount"],
            'key_id': settings.RAZORPAY_API_KEY
        }
        return render(request,'store/checkout.html',context)

def get_cities(request):
    state_name = request.GET.get('state_id')
    state_name = State.objects.get(state=state_name)
    cities = City.objects.filter(state=state_name).values_list('id', 'city')
    city_dict = dict(cities)
    
    print(city_dict)
    return JsonResponse(city_dict)

def get_pin(request):
    city_name = request.GET.get('city_id')
    city_name = City.objects.get(city=city_name)
    pincode = Pin_Code.objects.filter(city=city_name).values_list('id','pincode')
    pincode_dict = dict(pincode)
    print(pincode_dict)
    return JsonResponse(pincode_dict)

@login_required
def orderDetails(request,orderId):
    if request.method=='POST':
        return redirect("order_details")
    else:
        data = Category.objects.all()
        order = Order.objects.get(id=orderId)
        payment = Payment.objects.get(order=order)
        orderItems = OrderItem.objects.filter(order=orderId)
        biling = OrderBill.objects.filter(order=order)
        context={
            'data':data,
            'order':order,
            'payment':payment,
            'bill':biling,
            'orderItem':orderItems,
        }
        return render(request,'store/order-details.html',context)

@require_POST
def ratting(request):
    ratingvalue = request.POST.get('ratting')
    comment = request.POST.get('comment')
    productId = int(request.POST.get('productid'))
    product = Product.objects.get(pk=productId)
    custuser = Customeruser.objects.get(user=request.user)
    print(custuser)
    review,create = Review.objects.get_or_create(product=product,user=custuser)
    review.content = comment
    review.rating = ratingvalue
    print(review)
    review.save()
    
    return JsonResponse({'success': True})

def delete_ratting(request,product):
    product = Product.objects.get(id=product)
    user = Customeruser.objects.get(user=request.user)

    review = Review.objects.get(product=product,user=user)
    print(review)
    review.delete()
    return JsonResponse({'message': 'Review deleted successfully'})

def search_product(request):
    query = request.GET.get('query', '')
    if query:
        results = Category.objects.filter(title__icontains=query)
        catresults = [{'name': category.title,'id':category.id} for category in results]
        # Query products based on the search query
        results = Product.objects.filter(title__icontains=query)
        proresults = [{'name': product.title,'id':product.id} for product in results]

        serialized_results = catresults + proresults
        print(catresults)
        return JsonResponse({'results1': catresults,'results2':proresults})
    else:
        return JsonResponse({'results': []})
    
@csrf_exempt
def like(request,product_id):

    product=Product.objects.get(pk=product_id)
    liked=[]
    if request.user.is_authenticated:
        liked_item, created = LikedProduct.objects.get_or_create(user=request.user, Product=product)
        print(created)
        print(product)
        if created:
            liked_item.like =True;
            liked_item.save()
        else:
            liked_item.delete()
        
        likeId = LikedProduct.objects.filter(user=request.user)
        
        for likeitem in likeId:
            liked.append(likeitem.Product.id)
    else:
        liked = request.session.get('liked_products', [])

        if product_id in liked:
            liked.remove(product_id)
        else:
            liked.append(product_id)

        print(liked)
        request.session['liked_products'] = liked

    return JsonResponse({'like': liked}) 