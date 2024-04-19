from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe
# Create your models here.

class State(models.Model):
    state = models.CharField(max_length=20,unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.state

class City(models.Model):
    city = models.CharField(max_length=20,unique=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city

class Pin_Code(models.Model):
    pincode = models.IntegerField(unique=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pincode)
    
class Customeruser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    phone_one = models.BigIntegerField(blank=True, null=True)
    phone_second = models.BigIntegerField(blank=True, null=True)
    user_image = models.ImageField(upload_to="media/img/profile/",default="static/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def photo(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.user_image.url))
    photo.short_description= 'Image'
    photo.allow_tags  = True

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=50,null=False,unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    title = models.CharField(max_length=50,null=False,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to="media/img/product/")
    price = models.DecimalField(max_digits=10,decimal_places=2)
    offer_price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    shipping_charges = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    is_active = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, blank=True, null=True)

    def photo(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.product_image.url))
    photo.short_description= 'Image'
    photo.allow_tags  = True

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for cart_item in self.cart_item_set.all():
            cart_item.total_price = self.price * cart_item.quantity
            cart_item.save()

class ProductImage(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    img1 = models.ImageField(upload_to="media/img/multi-imge")
    img2 = models.ImageField(upload_to="media/img/multi-imge")
    img3 = models.ImageField(upload_to="media/img/multi-imge")

    def photo1(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.img1.url))
    photo1.short_description= 'Image1'
    photo1.allow_tags  = True

    def photo2(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.img2.url))
    photo2.short_description= 'Image2'
    photo2.allow_tags  = True

    def photo3(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.img3.url))
    photo3.short_description= 'Image3'
    photo3.allow_tags  = True


class ProductDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    common_name = models.CharField(max_length=50,blank=True, null=True,verbose_name="Common Name")
    color = models.CharField(max_length=50,blank=True, null=True,verbose_name="Color")
    plant_height = models.CharField(max_length=50,blank=True, null=True,verbose_name="Height")
    plant_spread = models.CharField(max_length=50,blank=True, null=True,verbose_name="Spread")
    weigth = models.CharField(max_length=50,blank=True, null=True,verbose_name="weigth")
    Material = models.CharField(max_length=50,blank=True, null=True)
    Length = models.CharField(max_length=50,blank=True, null=True)
    Compatibility = models.CharField(max_length=50,blank=True, null=True)
    Warranty = models.CharField(max_length=50,blank=True, null=True,verbose_name="Warranty Information")
    Country_of_Origin = models.CharField(max_length=50,blank=True, null=True,verbose_name="Country of Origin")
    
    def __str__(self):
        return self.product.title
        
class CareTips(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Watering = models.CharField(max_length=200,blank=True, null=True,verbose_name="Watering")
    Light  = models.CharField(max_length=200,blank=True, null=True,verbose_name="Light")
    Soil = models.CharField(max_length=200,blank=True, null=True,verbose_name="Soil")
    Fertilizing=models.CharField(max_length=200,blank=True, null=True,verbose_name="Fertilizing")
    Temperature = models.CharField(max_length=200,blank=True, null=True,verbose_name="Temperature")
    Seasonal_Care = models.CharField(max_length=200,blank=True, null=True,verbose_name="Seasonal Care")
    Instructions = models.CharField(max_length=300,blank=True, null=True,verbose_name="Care Instructions:")

    def __str__(self):
        return self.product.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_product = models.PositiveIntegerField(default=0)
    total_cart = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_totals(self):
        cart_items = self.cart_item_set.all()
        total_product=0
        for item in cart_items:
            total_product+=1
    
        total_cart = sum(item.discount_price for item in cart_items)
        self.total_product = total_product
        self.total_cart = total_cart
        self.save()
    
class Cart_item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.discount_price = self.product.offer_price * self.quantity
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.cart.update_totals()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_totals()
        
order_status={
    ('pending','Panding'),
    ('cancelled','Cancelled'),
    ('confirem','Confirm'),
    ('on the way','On the way'),
    ('delivered','Delivered')
}
payment={
    ('pending','Panding'),
    ('cancelled','cancelled'),
    ('confirm','Confirm')
}

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    address = models.TextField()
    landmark = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    pin_code = models.CharField(max_length=50,blank=True, null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    discount =models.DecimalField(max_digits=10,decimal_places=2)
    shipping_charges =models.DecimalField(max_digits=10,decimal_places=2)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10,choices=order_status,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def photo(self):
        return mark_safe('<img src="{}" width="100" height="100" style="border-radius:5px" />'.format(self.product.product_image.url))
    photo.short_description= 'Image'
    photo.allow_tags  = True

    def __str__(self):
        return f"{self.order.user.username}"    

class OrderBill(models.Model):
    billNo = models.CharField(max_length=10)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    address = models.TextField()
    landmark = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    pin_code = models.CharField(max_length=50,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    payment_id = models.CharField(max_length=50,blank=True, null=True,verbose_name="Online transaction ID")
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10,choices=payment,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Customeruser,on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    avg_rating = Review.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        product.rating = avg_rating
        product.save()

class LikedProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

CITY_CHOICE=(
    ('Ahemdabad','ahmdabad'),
    ('Rajkot','delhi')
)
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    address = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=20,blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    pin_code = models.CharField(max_length=50,blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address},{self.city},{self.state}- {self.pin_code}"


