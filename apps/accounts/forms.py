from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    password1=forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})))
    password2=forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm Password'})))

    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        required_fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Email'}),
        }