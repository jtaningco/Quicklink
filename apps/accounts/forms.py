from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User

class MerchantForm(ModelForm):
    password2=forms.CharField(label='Confirm Password', 
                            widget=forms.PasswordInput(attrs={
                            'class': 'input', 
                            'placeholder': 'Confirm Password'}))

    class Meta: 
        model = User
        fields = ['role', 'username', 'email', 'password', 'password2']
        required_fields = ['username', 'email', 'password', 'password2']

        widgets = {
            'role': forms.HiddenInput(attrs={
                'value':User.Types.MERCHANT}),
            'username': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={
                'class': 'input', 
                'placeholder': 'Enter Password'})
        }

        def __init__(self, *args, **kwargs):
            super(MerchantForm, self).__init__(*args, **kwargs)
            self.fields['role'].initial = User.Types.MERCHANT

class CustomerForm(ModelForm):
    password2=forms.CharField(label='Confirm Password', 
                            widget=forms.PasswordInput(attrs={
                            'class': 'input', 
                            'placeholder': 'Confirm Password'}))

    class Meta: 
        model = User
        fields = ['role', 'username', 'email', 'password', 'password2']
        required_fields = ['username', 'email', 'password', 'password2']

        widgets = {
            'role': forms.HiddenInput(attrs={
                'value':User.Types.CUSTOMER}),
            'username': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Username'}),
            'email': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={
                'class': 'input', 
                'placeholder': 'Enter Password'})
        }

        def __init__(self, *args, **kwargs):
            super(CustomerForm, self).__init__(*args, **kwargs)
            self.fields['role'].initial = User.Types.CUSTOMER