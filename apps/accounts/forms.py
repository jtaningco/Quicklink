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
        if name == 'delivery_schedule':
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

    # shop_delivery_schedule
    delivery_schedule = forms.IntegerField(widget=BinaryWidget(choices=(
        ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'),
        ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'),
        ('7', 'Sunday')
    )))

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
                        'class': 'input default', 
                        'placeholder': 'City'}),
                        choices=Address.CITIES)
    province=forms.ChoiceField(label='', 
                        widget=forms.Select(attrs={
                        'class': 'input default', 
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

    shop_cod=forms.BooleanField()

class ShopLogoForm(ModelForm):
    class Meta:
        model = ShopLogo
        fields = ['logo']
        required_fields = ['logo']

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