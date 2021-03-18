from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import *

# Create User
class CreateUserForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
                            'class': 'input default', 
                            'placeholder': 'Enter Password'}))

    password2=forms.CharField(widget=forms.PasswordInput(attrs={
                            'class': 'input default', 
                            'placeholder': 'Confirm Password'}))

    class Meta: 
        model = User
        fields = ('email',)

        widgets = {
            'email': forms.fields.EmailInput(attrs={
                'class':'input default',
                'placeholder': 'Email'})
        }

        def __init__(self, *args, **kwargs):
            super(CreateUserForm, self).__init__(*args, **kwargs)

    def validate_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['Passwords does not match.'],
                code='password_mismatch',
            )
        return True

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

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