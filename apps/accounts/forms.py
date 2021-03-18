from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import *

class MerchantForm(ModelForm):
    password2=forms.CharField(label='Confirm Password', 
                            widget=forms.PasswordInput(attrs={
                            'class': 'input', 
                            'placeholder': 'Confirm Password'}))

    class Meta: 
        model = User
        fields = ['role', 'email', 'password', 'password2']
        required_fields = ['email', 'password', 'password2']

        widgets = {
            'role': forms.HiddenInput(attrs={
                'value':User.Types.MERCHANT}),
            'email': forms.fields.EmailInput(attrs={
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
    # shop_delivery_schedule
    day_from = forms.ChoiceField(label='',
                                widget=forms.Select(attrs={
                                    'class': 'small-input', 
                                    'placeholder': 'Opening Day'}),
                                choices=OpenHours.WEEKDAYS)
    day_to = forms.ChoiceField(label='',
                                widget=forms.Select(attrs={
                                    'class': 'small-input', 
                                    'placeholder': 'Closing Day'}),
                                choices=OpenHours.WEEKDAYS)
    from_hour = forms.ChoiceField(label='',
                                widget=forms.Select(attrs={
                                    'class': 'small-input', 
                                    'placeholder': 'Open From'}),
                                choices=OpenHours.HOUR_OF_DAY_24)
    to_hour = forms.ChoiceField(label='',
                                widget=forms.Select(attrs={
                                    'class': 'small-input', 
                                    'placeholder': 'Open Until'}),
                                choices=OpenHours.HOUR_OF_DAY_24)

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
                        'class': 'input', 
                        'placeholder': 'City'}),
                        choices=Address.CITIES)
    province=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'class': 'small-input', 
                        'placeholder': 'Province'}),
                        choices=Address.PROVINCES)
    postal_code=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'small-input', 
                        'placeholder': 'Postal Code'}))
    
    # shop_links
    instagram=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Instagram Link'}),
                        required = False)
    facebook=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Facebook Link'}),
                        required = False)
    twitter=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Twitter Link'}),
                        required = False)

    class Meta:
        model = ShopInformation
        fields = ['shop_name', 
                'shop_contact_number', 
                'shop_username',
                'shop_cod']
        required_fields = ['shop_name', 
                'shop_contact_number', 
                'shop_username',
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

class ShopLogoForm(ModelForm):
    class Meta:
        model = ShopLogo
        fields = ['shop', 'logo']
        required_fields = ['shop', 'logo']

        widgets = {
            'shop': forms.HiddenInput(),
        }

class ShopAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['user','bank_name', 'cardholder_name', 'account_number']
        required_fields = ['bank_name', 'cardholder_name', 'account_number']

        widgets = {
            'cardholder_name': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Cardholder Name'}),
            'account_number': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Account Number'}),
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

class CustomerInformationForm(ModelForm):
    # shop_links
    instagram=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Instagram Link'}),
                        required = False)
    facebook=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input', 
                        'placeholder': 'Facebook Link'}),
                        required = False)

    class Meta:
        model = CustomerInformation
        fields = ['customer_name',
        'customer_contact_number',
        'customer_username']
        required_fields = ['customer_name',
        'customer_contact_number',
        'customer_username']

        widgets = {
            'customer_name': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Name'}),
            'customer_contact_number': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Mobile Number'}),
            'customer_username': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Username'}),
        }

class CustomerAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ["line1",
                "line2",
                "city",
                "province",
                "postal_code"]
        required_fields = ["line1",
                "line2",
                "city",
                "province",
                "postal_code"]

        widgets = {
            'line1': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Address Line 1'}),
            'line2': forms.fields.TextInput(attrs={
                    'class':'input',
                    'placeholder': 'Address Line 2'}),
            'city': forms.Select(attrs={
                    'class':'input',
                    'placeholder': 'City'}),
            'province': forms.Select(attrs={
                    'class':'small-input',
                    'placeholder': 'Province'}),
            'postal_code': forms.fields.TextInput(attrs={
                    'class':'small-input',
                    'placeholder': 'Postal Code'}),
        }

        choices = {
            'city': Address.CITIES,
            'province': Address.PROVINCES
        }

class CustomerAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ["bank_name",
                "cardholder_name",
                "account_number",
                "exp_date",
                "cvv"]
        widgets = {
            'cardholder_name': forms.fields.TextInput(attrs={
                'class':'input',
                'placeholder': 'Ex. Juan Dela Cruz'}),
            'account_number': forms.fields.TextInput(attrs={
                    'class':'input',
                    'placeholder': 'Ex. 1234 5678 9876 5432'}),
            'exp_date': forms.fields.TextInput(attrs={
                    'class':'small-input',
                    'placeholder': 'MM/YY'}),
            'cvv': forms.PasswordInput(attrs={
                    'class':'small-input',
                    'placeholder': '***'}),
        }

class NotificationsForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['sms', 'email']
        widgets = {
            'sms':forms.CheckboxInput(),
            'email':forms.CheckboxInput()
        }