from django import forms
from django.forms import ModelForm, inlineformset_factory
from apps.accounts.models import *
from apps.products.models import Product, Addon
from apps.orders.models import ProductOrder, OrderInformation
from django.utils.translation import ugettext_lazy as _

class PreviewOrderForm(ModelForm):
    class Meta: 
        model = ProductOrder
        fields = [ 
            'product',
            'quantity',
        ]
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
        }
        labels = {
            'product': '',
            'quantity' : '',
        }

class OrderForm(ModelForm):
    class Meta: 
        model = ProductOrder
        fields = [
            'order',
            'product',
            'quantity',
            'instructions',
        ]
        required_fields = [
            'quantity',
        ]

        widgets = {
            'order': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
            'instructions': forms.Textarea(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'Leave us a note! (Optional)'}),
        }

class CheckoutForm(forms.Form):
    # Personal Details
    name = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Name'}),)
    email = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Email'}),)
    contact_number = forms.CharField(label='',  
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Mobile Number'}),)

    # Shipping Address
    line1 = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Address Line 1'}))
    line2 = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Address Line 2'}))
    city = forms.ChoiceField(label='', 
        widget=forms.Select(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'City'}),
        choices=Address.CITIES)
    province = forms.ChoiceField(label='', 
        widget=forms.Select(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': 'Province'}),
        choices=Address.PROVINCES)
    postal_code = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': 'Postal Code'}))

    # Preferred Delivery Date
    delivery_date = forms.DateField(label='', 
        widget=forms.fields.DateInput())

    # Mode of Payment
    cardholder_name = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Ex. Juan Dela Cruz'}))
    card_number = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Ex. 1234 5678 9876 5432'}))
    expiry_date = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': 'MM/YY'}))
    cvv = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': '***'}))

    # Updates
    sms = forms.BooleanField(label='Receive SMS updates on order status',
        widget=forms.fields.CheckboxInput())
    email = forms.BooleanField(label='Receive email updates on order status',
        widget=forms.fields.CheckboxInput())

    def __init__(self, min_date, max_date, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['delivery_date'].widget.attrs.update({'min': min_date, 'max': max_date})