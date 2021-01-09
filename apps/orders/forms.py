from django import forms
from django.forms import ModelForm, inlineformset_factory
from apps.products.models import Product
from apps.orders.models import Order
from django.utils.translation import ugettext_lazy as _

class OrderForm(ModelForm):
    class Meta: 
        model = Order
        fields = [ 
            'quantity',
        ]
        widgets = {
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
        }
        labels = {
            'quantity' : '',
        }