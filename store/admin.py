from django.contrib import admin
from django.db.models import Count,Sum
# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin 
#Reports
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.template.loader import render_to_string
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle

def download_pdf(self,request,queryset):
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    pdf = canvas.Canvas(response,pagesize=letter)
    pdf.setTitle('PDF Report')

    headers = [field.verbose_name for field in self.model._meta.fields]
    data = [headers]

    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in self.model._meta.fields]
        data.append(data_row)
    
    table = Table(data)
    table.setStyle(TableStyle(
      [
        ('BACKGROUND',(0,0),(-1,0),colors.gray),
      ]
    ))

    canvas_width = 10
    canvas_height = 60

    table.wrapOn(pdf,canvas_width,canvas_height)
    table.drawOn(pdf,10,canvas_height - len(data))

    pdf.save()
    return response
download_pdf.short_description = "Download Selected items as PDF."

def generate_html_report(self, request, queryset):
    data = list(queryset.values())

    if data:
        headers = list(data[0].keys())
    else:
        headers = []
    html_string = render_to_string('admin/report.html', {'data': data,'headers':headers})
    return HttpResponse(html_string)
generate_html_report.short_description = "view report"

# Register your models here.
class StateAdmin(admin.ModelAdmin):
    list_display = ('state','is_active','created_at','updated_at')
    list_editable = ('is_active',)
    list_display_links = ('state',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('city','state','is_active','created_at','updated_at')
    list_filter = ('state',)
    list_editable = ('city','is_active')
    list_display_links = ('state',)

class PincodeAdmin(admin.ModelAdmin):
    list_display = ('pincode','city','created_at','updated_at')
    list_filter = ('city',)
    list_editable = ('pincode',)
    list_display_links = ('city',)

class CustUserAdmin(UserAdmin):
    action = [generate_html_report]

class CustomeruserAdmin(admin.ModelAdmin):
    list_display = ('photo','pk','user','phone_one','phone_second','user_image','updated_at')
    list_filter = ('updated_at','user')
    search_fields = ('user',)

    actions = [generate_html_report]

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','address','landmark','city','state','pin_code','create_at','update_at')
    list_filter = ('user',)
    list_editable = ('pin_code',)
    search_fields = ('pin_code','user')

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('fname','lname','phone','user','address','landmark','city','state','pin_code','create_at','update_at')
    list_filter = ('user',)
    list_editable = ('pin_code',)
    search_fields = ('pin_code','user')

    actions = [download_pdf]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','is_active','created_at','updated_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','category','is_active','created_at','updated_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('photo','title','price','quantity','shipping_charges','category','rating','is_active','create_at','update_at')
    list_filter = ('category','price','create_at')
    list_editable = ('is_active','price','quantity','rating','shipping_charges')
    search_fields = ('category','title')

    actions = [download_pdf]

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("Product","photo1","photo2","photo3")

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','total_product','total_cart')
    search_fields = ('user',)

    actions = [generate_html_report]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','product','quantity','total_price','discount_price')
    list_filter = ('product',)
    search_fields = ('cart',)

    actions = [generate_html_report]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','fname','lname','phone','address','landmark','city','state','pin_code','discount','shipping_charges','amount','total_amount','status','created_at')
    list_editable = ('status',)

    actions = [generate_html_report]

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("payment_method","payment_id","amount","order","created_at","updated_at")

    actions = [generate_html_report]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('photo','order','product','discount_price','price','quantity','subtotal')

    actions = [generate_html_report]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product','user','content','rating','created_at')

    actions = [generate_html_report]
    
class BillAdmin(admin.ModelAdmin):
    list_display = ('order','fname','lname','address','landmark','city','state','pin_code')

    actions = [generate_html_report]

class LikeProductAdmin(admin.ModelAdmin):
    list_display = ('user','Product','like')

    actions = [generate_html_report]

   
admin.site.register(State,StateAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Pin_Code,PincodeAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductDetails)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(CareTips)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Cart_item,CartItemAdmin)
admin.site.register(Customeruser,CustomeruserAdmin)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(OrderBill,BillAdmin)
admin.site.register(LikedProduct,LikeProductAdmin)
