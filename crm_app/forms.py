from django import forms
from django .contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from .models import Record



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'password1' , 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'category' , 'phone' , 'length' , 'weight' , 'address']


class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'category', 'phone', 'length', 'weight', 'address']
