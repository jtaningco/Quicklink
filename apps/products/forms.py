from django import forms
from django.forms import ModelForm 
from apps.products.models import Product
from django.utils.translation import ugettext_lazy as _

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'productImage',
            'stock',
            'size',
            'price',  
            'addon', 
            'instructions',
        ]

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class':'input default',
                'placeholder': 'Ex. Chocolate Chip Cookies'}),
            
            'description': forms.fields.TextInput(attrs={
                'class':'large-input default',
                'placeholder': 'Describe your product for your customers to see!'}),

            'stock': forms.RadioSelect(attrs={
                'class':'radio',
                'empty_label': None }), 

            'size': forms.fields.TextInput(attrs={
                'class':'small-input default',
                'placeholder': 'Ex. 1 Dozen'}),
            
            'price': forms.fields.TextInput(attrs={
                'class':'small-input default',
                'placeholder': 'Php'}),
            
            'addon': forms.fields.TextInput(attrs={\
                'class':'small-input default',
                'placeholder': 'Additional Chocolate Chip'}),
            
            'instructions': forms.fields.TextInput(attrs={
                'class':'large-input default',
                'placeholder': 'List them down here!'}),
        }

        labels = {
            'name' : 'Name',
            'description' : 'Description',
            'productImage' : '',
            'stock' : 'Stocks',
            'size' : 'Available Sizes or Servings',
            'price' : '',
            'addon' : 'Possible Add-Ons',
            'instructions' : 'Any special instructions, allergens, etc.?'
        }
