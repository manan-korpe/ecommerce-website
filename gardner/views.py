from django.shortcuts import render,redirect
from django.http import JsonResponse
from gardner.models import *
from store.models import *
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import ast
#email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def gardnerlist(request):
     data = Category.objects.all()
     service = Service.objects.all()
     context = {
          'data':data,
          "services":service,
     }
     return render(request,'gardner/gardnerlist.html',context)

@login_required
def booking(request,gardnerid=None):
    Category_list= Category.objects.all()
    gardner = Gardner.objects.get(pk=gardnerid)
    if request.method == "POST":
            date_str = request.POST.get("date")
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            time_str = request.POST.get("slot-time")
            if time_str == "":
                 messages.error(request,"Select time-slot for gardaner booking")

                 return redirect("booking",gardnerid)
            time = datetime.strptime(time_str, '%H:%M').time()

            fname = request.POST.get("fname")
            lname = request.POST.get("lname")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            area = request.POST.get("area")
            city = request.POST.get("city")
            state = request.POST.get("state")
            postCode = request.POST.get("post-code")
            
            booking_instance = Booking(
            gardner=gardner,
            customer=request.user,  
            fname=fname,
            lname=lname,
            phone=phone,
            email=email,
            area=area,
            city=city,
            state=state,
            pin_code=postCode,
            booking_date=date,
            booking_time=time,
            service_name=gardner.service,  
            service_amount=gardner.price,  
            service_offer_amount=gardner.offer_price,
          )
            context={
                 "booking_instance":booking_instance,
            }
            
            #Custemer email
            html_message = render_to_string('template/Email/booking_confirm.html',context)
            plain_email = strip_tags(html_message)
            message = EmailMultiAlternatives(
                 subject='Booking Confirmation',
                 body=plain_email,
                 from_email=settings.EMAIL_HOST_USER,
                 to=[email]
            )
            message.attach_alternative(html_message,'text/html')
            message.send()
            
            #Gardner Email
            html_message = render_to_string('template/Email/gardner_confirm.html',context)
            plain_email = strip_tags(html_message)
            message = EmailMultiAlternatives(
                 subject='Service Details',
                 body=plain_email,
                 from_email=settings.EMAIL_HOST_USER,
                 to=[gardner.email]
            )
            message.attach_alternative(html_message,'text/html')
            message.send()
            #close email sending logic----------------------------------------------

            booking_instance.save()
            messages.success(request,"booking successfully done")
            return redirect("gardnerlist")
    else:
      state = State.objects.all()
      date = request.GET.get('date')
      print(date)
      start_time = datetime.strptime('12:00', '%H:%M')
      end_time = datetime.strptime('18:00', '%H:%M')
      time = time_to_slot_duration(str(gardner.service_time))

      slots = generate_time_slots(start_time, end_time, time)
      
      current_date = datetime.now()
      today_date = current_date.strftime("%y-%m-%d")

      if request.method == "GET" and date != None:
           date = datetime.strptime(date, '%Y-%m-%d').date()
           bookinglist = Booking.objects.filter(booking_date=date) 
           print(bookinglist)
           print("booking name")
           bookedTime = []
           bt =[]
           nbt = []
           print(slots)
           for n in bookinglist:
                bookedTime.append(n.b_time.strftime('%H:%M'))

           for time in slots:
                if time in bookedTime:
                     bt.append(time)
                else:
                     nbt.append(time)
           slots = nbt 
           print(slots)
                
      context={
           "data":Category_list,
           "state":state,
            "gardner":gardner,
            "slots":slots,
            "date":today_date,
            "city":CITY_CHOICE,
      }
      return render(request, 'gardner/gardnerBooking.html',context)


def dateslot(request):
     service = request.GET.get("service")
     date = request.GET.get('date')
     slots = request.GET.get('slots')
     print(service,date,slots)

     json_data_slot = json.loads(slots)
     json_data_slot = ast.literal_eval(json_data_slot)

     date = datetime.strptime(date, '%Y-%m-%d').date()
     gardner = Gardner.objects.get(id=service)
     bookinglist = Booking.objects.filter(gardner=gardner,booking_date=date)
     bookedTime = []
     avl_slot = []

     for n in bookinglist:
          bookedTime.append(n.booking_time.strftime('%H:%M'))     
     for slot in json_data_slot:
          if slot not in bookedTime:
               avl_slot.append(slot)
     return  JsonResponse({'success':True,'avl_slot':avl_slot,'not_avl_slot':bookedTime})

'''-------------start------generate----slot--------------------'''

def time_to_slot_duration(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    
    total_minutes = hours * 60 + minutes
    
    return total_minutes

def generate_time_slots(start_time, end_time, slot_duration):
    current_time = start_time
    time_slots = []
    
    while current_time < end_time:
        time_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=slot_duration)

    return time_slots

'''-------------End------generate----slot--------------------'''