from django import forms
from django.forms import ModelForm, inlineformset_factory
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
            'size',
            'addons',
            'quantity',
            'instructions',
        ]
        required_fields = [
            'product',
            'size',
            'quantity',
        ]

        widgets = {
            'order': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'size': forms.RadioSelect(),
            'addons': forms.CheckboxSelectMultiple(),
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
            'instructions': forms.Textarea(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'Leave us a note! (Optional)'}),
        }

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['size'].queryset = self.fields['size'].queryset.filter(product=product)
            self.fields['addons'].queryset = self.fields['addons'].queryset.filter(product=product)