from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="media/img/GardnerList/",blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SubService(models.Model):
    title = models.CharField(max_length=20)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Gardner(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="media/img/GardnerService/",blank=True, null=True)
    service = models.ForeignKey(SubService,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    offer_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True, null=True)
    service_time = models.TimeField()
    service_type = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

CHOICE_STATUS={
    ('pending','Panding'),
    ('cancelled','Cancelled'),
    ('completed','Completed')
}

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    gardner = models.ForeignKey(Gardner,on_delete=models.CASCADE,blank=True,null=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    area = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=20)
    booking_date = models.DateField(auto_now_add=False)  # Adjust auto_now_add as needed
    booking_time = models.TimeField()
    service_name = models.ForeignKey(SubService, on_delete=models.CASCADE)
    service_amount= models.DecimalField(max_digits=10, decimal_places=2)
    service_offer_amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=10,choices=CHOICE_STATUS,default="pending")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)

