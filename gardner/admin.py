from django.contrib import admin
from gardner.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string

def generate_html_report(self, request, queryset):
    data = list(queryset.values())

    if data:
        headers = list(data[0].keys())
    else:
        headers = []
    html_string = render_to_string('admin/report.html', {'data': data,'headers':headers})
    return HttpResponse(html_string)
generate_html_report.short_description = "view report"


class ServiceAdmin(admin.ModelAdmin):
      list_display = ("title","is_active","created_at","updated_at")
      actions =(generate_html_report,)

class SubServiceAdmin(admin.ModelAdmin):
      list_display = ("service","title","is_active","created_at","updated_at")
      actions =(generate_html_report,)

class GardnerAdmin(admin.ModelAdmin):
      list_display = ("service","price","offer_price","service_time","service_type","name","email","phone","description")

class BoolingAdmin(admin.ModelAdmin):
     list_display = ("customer","gardner","fname","lname","phone","email","area","city","state","pin_code","booking_date","booking_time","service_name","service_amount","service_offer_amount","status","created","update")
     actions =(generate_html_report,)
     list_editable = ("status",)

admin.site.register(Service,ServiceAdmin)
admin.site.register(SubService,SubServiceAdmin)
admin.site.register(Gardner,GardnerAdmin)
admin.site.register(Booking,BoolingAdmin)
