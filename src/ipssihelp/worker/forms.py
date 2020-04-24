from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    address1 = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    city = forms.CharField(required=True)

class LoginWorkerForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label='password',
        strip=False
    )

class ContactForm(forms.Form):
    content = forms.CharField(required=True)
