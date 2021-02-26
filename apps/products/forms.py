from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import Textarea
from apps.products.models import *
from django.utils.translation import ugettext_lazy as _

# Initial Product Form
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'image',
            'stock',
            'days',
            'time',
            'schedule',
            'orders',
            'instructions',
        ]

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class':'input default subtitle',
                'placeholder': 'Ex. Chocolate Chip Cookies'}),
            
            'description': forms.Textarea(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'Describe your product for your customers to see!'}),

            'stock': forms.fields.TextInput(attrs={
                'class':'small-input disabled subtitle',
                'placeholder': '1'}),

            'days': forms.fields.NumberInput(attrs={
                'class':'smallest-input disabled subtitle',
                'placeholder': '0'}),

            'time': forms.fields.TextInput(attrs={
                'class':'smallest-input disabled subtitle',
                'placeholder': '1:00 PM'}),

            'schedule': forms.fields.TextInput(attrs={
                'class':'input default subtitle',
                'placeholder': 'Saturdays'}),

            'orders': forms.fields.NumberInput(attrs={
                'class':'smallest-input disabled subtitle',
                'placeholder': '0'}),
            
            'instructions': forms.Textarea(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'List them down here!'}),
        }

# FORMSET DRAFTS
# The formset for editing the size and prices that belong to a product
SizeFormset = inlineformset_factory(
                    Product,
                    Size,
                    can_delete=False,
                    fields=('size', 'price_size'),
                    widgets={
                        'size': forms.fields.TextInput(attrs={
                            'class':'small-input default subtitle',
                            'placeholder': 'Ex. 1 Dozen'}),

                        'price_size': forms.fields.NumberInput(attrs={
                            'class':'small-input default subtitle',
                            'placeholder': 'Php'}),
                    },
                    labels={
                        'size':'',
                        'price_size':'',
                    },
                    extra=2
                )

AddonFormset = inlineformset_factory(
                    Product,
                    Addon,
                    can_delete=False,
                    fields=('addon', 'price_addon'),
                    widgets={
                        'addon': forms.fields.TextInput(attrs={
                            'class':'small-input default subtitle',
                            'placeholder': 'Additional Chocolate Chip'}),

                        'price_addon': forms.fields.NumberInput(attrs={
                            'class':'small-input default subtitle',
                            'placeholder': 'Php'}),
                    },
                    labels={
                        'addon':'',
                        'price_addon':'',
                    }, 
                    extra=1
                )