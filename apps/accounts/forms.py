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

# For Delivery Dates
# See here for more information: https://stackoverflow.com/questions/19645227/django-create-multiselect-checkbox-input
# https://stackoverflow.com/questions/3663898/representing-a-multi-select-field-for-weekdays-in-a-django-model
class BinaryWidget(forms.CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        value = super(BinaryWidget, self).value_from_datadict(data, files, name)
        if name == 'delivery_days':
            value = sum([2**(int(x)-1) for x in value])
        return value

class ShopInformationForm(forms.Form):
    # Shop Details
    shop_name = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Shop Name'}),)
    shop_contact_number = forms.CharField(label='',  
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Contact Number'}),)
    shop_username = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Shop Quicklink Username'}),)
    shop_email = forms.EmailField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Display Email Address'}),)

    # shop_address
    line1=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Address Line 1'}))
    line2=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Address Line 2'}))
    city=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'class': 'wide input default', 
                        'placeholder': 'City'}),
                        choices=Address.CITIES)
    province=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'class': 'wide input default', 
                        'placeholder': 'Province'}),
                        choices=Address.PROVINCES)
    postal_code=forms.CharField(label='', 
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Postal Code'}))
    
    # shop_links
    instagram=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Instagram Link'}),
                        required = False)
    facebook=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Facebook Link'}),
                        required = False)
    twitter=forms.URLField(label='',
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Twitter Link'}),
                        required = False)

class ShopLogoForm(ModelForm):
    class Meta:
        model = ShopLogo
        fields = ['logo']
        required_fields = ['logo']

class ShopSettingsForm(forms.Form):
    ## Shop COD
    # shop.shop_general_settings.shop_cod
    shop_cod=forms.BooleanField(required=False)

    ## Order Cut-Off
    # shop.shop_general_settings.cutoff_days
    cutoff_days = forms.IntegerField(label='',
        required=False,
        widget=forms.fields.NumberInput(attrs={
        'class':'input default disabled subtitle',
        'placeholder': '0'}),
    )
    
    # shop.shop_general_settings.cutoff_time
    cutoff_time = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'wide input default subtitle'}),
        choices=ShopGeneralSettings.HOUR_OF_DAY_24,
        initial=ShopGeneralSettings.HOUR_OF_DAY_24[16],
        required=False
    )

    ## Delivery Schedule
    # shop.shop_general_settings.delivery_days
    delivery_days = forms.IntegerField(label='',
        widget=BinaryWidget(choices=(
        ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'),
        ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'),
        ('7', 'Sunday')
    )))

    # shop.shop_general_settings.delivery_from_hour
    from_hour = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'wide input default subtitle'}),
        choices=ShopGeneralSettings.HOUR_OF_DAY_24,
        initial=ShopGeneralSettings.HOUR_OF_DAY_24[12]
    )

    # shop.shop_general_settings.delivery_from_hour
    to_hour = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'wide input default subtitle'}),
        choices=ShopGeneralSettings.HOUR_OF_DAY_24,
        initial=ShopGeneralSettings.HOUR_OF_DAY_24[18]
    )

class DeliverySettingsForm(forms.Form):
    # shop.shop_delivery_settings
    seller_books=forms.BooleanField(required=False,
    widget=forms.CheckboxInput())
    buyer_books=forms.BooleanField(required=False,
    widget=forms.CheckboxInput())
    buyer_picks_up=forms.BooleanField(required=False,
    widget=forms.CheckboxInput())

    # shop.info_shop.shop_delivery_fees
    shop_delivery_fees = forms.CharField(label='',
        required=False,
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Fixed Delivery Fees'}),
    )

    # shop.shop_delivery_settings
    line1=forms.CharField(label='', required=False,
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Address Line 1'}))
    line2=forms.CharField(label='', required=False,
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Address Line 2'}))
    city=forms.ChoiceField(label='', required=False,
                        widget=forms.Select(attrs={
                        'class': 'wide input default', 
                        'placeholder': 'City'}),
                        choices=Address.CITIES)
    province=forms.ChoiceField(label='', required=False,
                        widget=forms.Select(attrs={
                        'class': 'wide input default', 
                        'placeholder': 'Province'}),
                        choices=Address.PROVINCES)
    postal_code=forms.CharField(label='', required=False,
                        widget=forms.fields.TextInput(attrs={
                        'class': 'input default', 
                        'placeholder': 'Postal Code'}))

    def clean_delivery_fees(self):
        fees = self.cleaned_data['shop_delivery_fees']
        try:
            response = fees.split()
            numbers = []
            for num in response:
                try:
                    if num.isdigit() or isinstance(float(num), float):
                        numbers.append(num)
                except: continue
            fees = float(''.join(numbers))
        except:    
            raise forms.ValidationError(_('Invalid format in delivery fees.'), code='invalid_format')
        return fees

class ShopAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'cardholder_name', 'account_number']
        required_fields = ['bank_name', 'cardholder_name', 'account_number']

        widgets = {
            'bank_name': forms.Select(attrs={
                'class':'wide input default'}),
            'cardholder_name': forms.fields.TextInput(attrs={
                'class':'input default',
                'placeholder': 'Cardholder Name'}),
            'account_number': forms.fields.TextInput(attrs={
                'class':'input default',
                'placeholder': 'Account Number'}),
        }

    def __init__(self, *args, **kwargs):
        super(ShopAccountForm, self).__init__(*args, **kwargs)

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