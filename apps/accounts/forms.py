from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User, ShopInformation

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

class ShopInformationForm(ModelForm):
    # shop_address
    line1=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Address Line 1'}))
    line2=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Address Line 2'}))
    city=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'placeholder': 'City'}))
    province=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'placeholder': 'Province'}))
    postal_code=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'small input', 
                        'placeholder': 'Postal Code'}))
    
    # shop_links
    instagram=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Instagram Link'}))
    facebook=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Facebook Link'}))
    twitter=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Twitter Link'}))

    class Meta:
        model = ShopInformation
        fields = ['shop_name', 
                'shop_contact_number', 
                'shop_username',
                'shop_delivery_schedule', 
                'shop_address',
                'shop_links',
                'shop_cod']
        required_fields = ['shop_name', 
                'shop_contact_number', 
                'shop_username',
                'shop_delivery_schedule', 
                'shop_address',
                'shop_cod']

        widgets = {
            'shop_name': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Shop Name'}),
            'shop_contact_number': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': '+639161611616'}),
            'shop_username': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Shop Quicklink Username'}),
        }

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