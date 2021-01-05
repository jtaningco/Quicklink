from django import forms
from django.forms import ModelForm 
from apps.products.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'productImage', 
            'stock',
            'price', 
            'addon', 
            'instructions',
        ]
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class':'input default',
                'placeholder': 'Ex. Chocolate Chip Cookies'}),
            
            'description': forms.fields.EmailInput(attrs={
                'class':'large-input default',
                'placeholder': 'Describe your product for your customers to see!'}),
            
            'stock': forms.fields.TextInput(attrs={
                'class':'small-input default',
                'placeholder': 'Ex. 1 Dozen'}),
            
            'price': forms.fields.TextInput(attrs={
                'class':'small-input default',
                'placeholder': 'Php'}),
            
            'addon': forms.fields.TextInput(attrs={
                'class':'small-input default',
                'placeholder': 'Additional Chocolate Chip'}),
            
            'instructions': forms.fields.TextInput(attrs={
                'class':'large-input default',
                'placeholder': 'List them down here!'}),
        }
