from django import forms
from django.forms import ModelForm, inlineformset_factory
from apps.accounts.models import *
from apps.products.models import Product, Addon
from apps.orders.models import ProductOrder
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

class CheckoutForm(ModelForm):
    class Meta:
        model = CustomerInformation
        fields = [
            'customer_name', 'customer_email', 'customer_contact_number',
        ]
        required_fields = [
            'customer_name', 'customer_email', 'customer_contact_number',
        ]


# FORMSET DRAFTS
# The formset for filling out customer information and shipping address
CustomerInfoFormset = inlineformset_factory(
                    User,
                    CustomerInformation,
                    can_delete=False,
                    fields=('customer_name', 'customer_email', 'customer_contact_number'),
                    widgets={
                        'customer_name': forms.fields.TextInput(attrs={
                            'class':'input default subtitle',
                            'placeholder': 'Name'}),

                        'customer_email': forms.fields.TextInput(attrs={
                            'class':'input default subtitle',
                            'placeholder': 'Email'}),
                        'customer_contact_number': forms.fields.TextInput(attrs={
                            'class':'input default subtitle',
                            'placeholder': 'Mobile Number'}),
                    },
                    labels={
                        'customer_name':'',
                        'customer_email':'',
                        'customer_contact_number':'',
                    },
                    extra=1
                )

ShippingFormset = inlineformset_factory(
                    User,
                    Address,
                    can_delete=False,
                    fields=('line1', 'line2', 'city', 'province', 'postal_code'),
                    widgets={
                        'line1': forms.fields.TextInput(attrs={
                            'class':'input default subtitle',
                            'placeholder': 'Address Line 1'}),

                        'line2': forms.fields.TextInput(attrs={
                            'class':'input default subtitle',
                            'placeholder': 'Address Line 2 (Optional)'}),
                        'city':
                    },
                    labels={
                        'customer_name':'',
                        'customer_email':'',
                        'customer_contact_number':'',
                    },
                    extra=1
                )