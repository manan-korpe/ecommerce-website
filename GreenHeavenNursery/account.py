from django.shortcuts import render,redirect
from django.contrib import messages
from store.models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import sign_in_form,Forget_Password_Form,OtpVerify_Form,Forget_new_password_Form
from django.core.mail import EmailMultiAlternatives,send_mail
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
import random,string

def sign_in(request):
    if request.method == 'POST':
        fm = sign_in_form(request.POST)
        if fm.is_valid():
            fm.save()
            
            uname = fm.cleaned_data['username']
            uemail = fm.cleaned_data['email']

            #crate new user cart 
            saved_user = User.objects.get(username=uname) 
            cart = Cart(user=saved_user)
            cart.save()
            
            #crate new Custuser 
            custuser = Customeruser(user=saved_user)
            custuser.save()

            #email sending logic----------------------------------------------
            html_message = render_to_string('template/Email/register_email.html')
            plain_email = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject='welcome to Green Heaven Nursery',
                body=plain_email,
                from_email=settings.EMAIL_HOST_USER,
                to=[uemail]
            )

            message.attach_alternative(html_message,'text/html')
            message.send()
            #close email sending logic----------------------------------------------

            fm = sign_in_form()
            messages.success(request,'Account Created Successfully !!')
            return redirect('login')
    else:
        fm = sign_in_form()
        
    return render(request,'authentication/register.html',{'form':fm})

def user_login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return redirect('/admin/')
                else:                
                    return redirect('home')
            else:
                return redirect('login')
    else:
        fm = AuthenticationForm()
    return render(request,'authentication/login.html',{'form':fm})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_change_Passwordd(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'Password change successfully...')
            fm = PasswordChangeForm(user=request.user)
            messages.success(request,"Password Change succesfully..")
            return redirect("logout")
            
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request,'authentication/changepassword.html',{'form':fm})

def forget_password(request):
    if request.method == "POST":
        form = Forget_Password_Form(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                OTP = random.randint(111111,999999)

                subject = 'Password REset OTP'
                message = "Your OTP is, " + str(OTP)
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)
                
                request.session["reset_password_OTP"] = OTP
                request.session["reset_password_EMAIL"] = email
                request.session.set_expiry(900)
                return redirect("forget_password_otpverify")
            
    else:
        form = Forget_Password_Form()
    return render(request,'authentication/forget_password_form.html',{'form':form})

def forget_password_otpverify(request):
    if request.method == 'POST':
        form = OtpVerify_Form(request.POST)
        otp = request.POST.get('otp')
        session_otp = request.session.get('reset_password_OTP')
        if str(otp) == str(session_otp):
            return redirect('forget_ResetPassword')
        else:
            messages.error(request,"Please enter valid OTP")
            return redirect('forget_password_otpverify')
    else:
        form = OtpVerify_Form()
    return render(request,'authentication/forget_password_otpverify_form.html',{'form':form})

def forget_ResetPassword(request):
    if request.method == "POST":
        form = Forget_new_password_Form(request.POST)
        if form.is_valid():
            password = request.POST.get('password1')
            email_var = request.session.get('reset_password_EMAIL')
            user = User.objects.get(email=email_var)
            user.set_password(password)
            user.save()
            request.session.delete()
            return redirect('login')
    else:
        form = Forget_new_password_Form()
    return render(request,"authentication/forget_password_set.html",{'form':form})    
