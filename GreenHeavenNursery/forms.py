from django import forms
from store.models import *
from store.models import ShippingAddress,Customeruser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.forms import User,UserCreationForm
from django.core.validators import EmailValidator,RegexValidator

class Custuserform(forms.Form):
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'readonly':'readonly','placeholder':"First Name"}))
    last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.EmailField(validators=[EmailValidator(message='')],widget=forms.TextInput(attrs={'readonly':'readonly'}))
    phone_one = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','placeholder':"Phone1"}),validators=[RegexValidator(regex=r'^[6-9]\d{9}$',message='Enter valid 10-digite Mobile Number')])
    phone_second = forms.CharField(required=False,validators=[RegexValidator(regex=r'^[6-9]\d{9}$',message='Enter valid 10-digite Mobile Number')],widget=forms.TextInput(attrs={'readonly':'readonly','placeholder':"Phone2"}))

    def clean(self):
        cleaned_data = super().clean()
        phone_one = cleaned_data.get('phone_one')
        phone_second = cleaned_data.get('phone_second')

        if not phone_one and not phone_second:
            raise ValidationError("At least one phone number is required")
        
        cleaned_data['phone_one'] = None if phone_one == '' else phone_one
        cleaned_data['phone_second'] = None if phone_second == '' else phone_second

        return cleaned_data

class sign_in_form(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.', required=True)
    first_name = forms.CharField(max_length=20, help_text='Required. Enter a valid first name.', required=True)
    last_name = forms.CharField(max_length=20, help_text='Required. Enter a valid last   name.', required=True)
    
    class Meta:
       model = User
       fields =['username','first_name','last_name','email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                self.add_error('email', 'This email address is already in use.')
        return cleaned_data

class Forget_Password_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control',}))
    
    class Meta:
        model = User
        fields = ['email']

class OtpVerify_Form(forms.Form):
     otp = forms.CharField(label='OTP',required=True, error_messages={'required':'Please enter OTP'} ,max_length=6)
     
class Forget_new_password_Form(forms.Form):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("confirm_password")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
   
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Customeruser
        fields = ['user_image']
        widgets = {
            'user_image': forms.FileInput(attrs={
                'data-parsley-pattern': '^[7-9][0-9]{9}$',
                'data-parsley-pattern-message': 'Please enter a valid mobile phone number.',
                'accept':'.jpg, .jpeg',
                "id":"imageupload"
            })
        }
    
    def clean_user_image(self):
        user_image = self.cleaned_data.get('user_image', False)
        if user_image:
            # Check if the file extension is allowed
            if not user_image.name.endswith(('.jpg', '.jpeg')):
                raise forms.ValidationError("Only JPEG/JPG files are allowed.")
        return user_image



class ShippingForms(forms.ModelForm):
    STATE_CHOICES = [(state.state, state.state) for state in State.objects.all()] 

    fname = forms.CharField(label='First Name', required=True, widget=forms.TextInput(attrs={'placeholder': 'first name'}))
    lname = forms.CharField(label='Last Name', required=True, widget=forms.TextInput(attrs={'placeholder': 'last name'}))
    phone = forms.CharField(label='Phone', required=True, widget=forms.TextInput(attrs={'placeholder': 'phone number','data-parsley-pattern': '^[7-9][0-9]{9}$','data-parsley-pattern-message': 'Please enter a valid mobile phone number.'}))
    address = forms.CharField(label='Address', required=True, widget=forms.TextInput(attrs={'placeholder': 'address'}))
    landmark = forms.CharField(label='Landmark', required=True, widget=forms.TextInput(attrs={'placeholder': 'landmark'}))
    state = forms.ChoiceField(choices=STATE_CHOICES,widget=forms.Select(attrs={'placeholder': 'Select your State',
        'data-parsley-required': "true",
        'data-parsley-required-message': "Select State",
        'onchange': 'cgnc(this,"#city");'}))

    class Meta:
        model = ShippingAddress
        fields = ['fname','lname','phone','address', 'landmark','state', 'city', 'pin_code']
        widgets = {
            'phone': forms.TextInput(attrs={
                'data-parsley-pattern': '^[7-9][0-9]{9}$',
                'data-parsley-pattern-message': 'Please enter a valid mobile phone number.'
            }),
           
            
            'city': forms.Select(attrs={
                'placeholder': 'Select your city',
                'data-parsley-required':"true",
                'data-parsley-required-message':"Select City",
                'id':'city',
                'onchange':"cgnp(this,'#post-code');"
            }),
            'pin_code': forms.Select(attrs={
                'data-parsley-required':"true",
                'data-parsley-required-message':"Select Pin code",
                'id':'post-code',
            })
        }
        
