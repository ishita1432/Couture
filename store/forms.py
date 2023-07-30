from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {'class':'form control w-100 ','placeholder':'Enter username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs = {'class':'form control w-100','placeholder':'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form control w-100','placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form control w-100','placeholder':'Confirm password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
