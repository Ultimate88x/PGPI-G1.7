from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['name', 'surnames', 'email', 'phone', 'address', 'city', 'zip_code', 'password1', 'password2']

class CustomerLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')