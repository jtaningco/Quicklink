from django import forms
from django.forms import ModelForm, inlineformset_factory
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
            'stock',
            'orders',
            'instructions',
        ]

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class':'input default subtitle',
                'placeholder': 'Ex. Chocolate Chip Cookies'}),
            
            'description': forms.Textarea(attrs={
                'class':'input large-input default subtitle',
                'placeholder': 'Describe your product for your customers to see!'}),

            'stock': forms.fields.NumberInput(attrs={
                'class':'input default disabled subtitle',
                'placeholder': '100'}),

            'orders': forms.fields.TextInput(attrs={
                'class':'input default disabled subtitle',
                'placeholder': '10'}),
            
            'instructions': forms.Textarea(attrs={
                'class':'input large-input default subtitle',
                'placeholder': 'List them down here!'}),
        }

# FORMSET DRAFTS
# The formset for placing images
ImageFormset = inlineformset_factory(
                    Product,
                    Image,
                    can_delete=False,
                    fields=('image','default'),
                    extra=3,
                )

# The formset for editing the size and prices that belong to a product
SizeFormset = inlineformset_factory(
                    Product,
                    Size,
                    can_delete=False,
                    fields=('size', 'price_size'),
                    widgets={
                        'size': forms.fields.TextInput(attrs={
                            'class':'input default subtitle js-size-input',
                            'placeholder': 'Ex. 1 Dozen'}),

                        'price_size': forms.fields.NumberInput(attrs={
                            'class':'input default subtitle js-size-price-input',
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
                            'class':'input default subtitle js-addon-input',
                            'placeholder': 'Additional Chocolate Chip'}),

                        'price_addon': forms.fields.NumberInput(attrs={
                            'class':'input default subtitle js-addon-price-input',
                            'placeholder': 'Php'}),
                    },
                    labels={
                        'addon':'',
                        'price_addon':'',
                    }, 
                    extra=1
                )