from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import Textarea
from apps.products.models import Product
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
            'size',
            'price',
            'addon',
            'addon_price',
            'instructions',
        ]

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'class':'input default subtitle',
                'placeholder': 'Ex. Chocolate Chip Cookies'}),
            
            'description': forms.fields.TextInput(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'Describe your product for your customers to see!'}),

            'stock': forms.RadioSelect(attrs={
                'class':'radio',
                'empty_label': None }), 
                
            'size': forms.fields.TextInput(attrs={
                'class':'small-input default subtitle',
                'placeholder': 'Ex. 1 Dozen'}),

            'price': forms.fields.NumberInput(attrs={
                'class':'small-input default subtitle',
                'placeholder': 'Php'}),
            
            'addon': forms.fields.TextInput(attrs={\
                'class':'small-input default subtitle',
                'placeholder': 'Additional Chocolate Chip'}),

            'addon_price': forms.fields.NumberInput(attrs={
                'class':'small-input default subtitle',
                'placeholder': 'Php'}),
            
            'instructions': forms.fields.TextInput(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'List them down here!'}),
        }

        labels = {
            'name' : _('Name'),
            'description' : _('Description'),
            'image' : _(''),
            'stock' : _('Stocks'),
            'size' : _('Available Sizes or Servings'),
            'price' : _(''),
            'addon' : _('Possible Add-Ons'),
            'addon_price' : _(''),
            'instructions' : _('Any special instructions, allergens, etc.?')
        }

# Formset Draft for adding more sizes and prices

# The formset for editing the size and prices that belong to a product
# SizeFormset = inlineformset_factory(
#                     Product, 
#                     Sizes, 
#                     fields=('size', 'price'), 
#                     extra=1)

# class BaseProductFormset(BaseInlineFormSet):
#     # The base formset for editing Products belonging to a User, and the
#     # size and prices available for those Products.
    
#     def add_fields(self, form, index):
#         super().add_fields(form, index)

#         form.nested = SizeFormset(
#                             instance=form.instance,
#                             data=form.data if form.is_bound else None,
#                             files=form.files if form.is_bound else None,
#                             prefix='sizes-%s-%s' % (
#                                 form.prefix,
#                                 SizeFormset.get_default_prefix()),
#                             )
    
#     def is_valid(self):
#         # Validate the nested formsets.
#         result = super().is_valid()

#         if self.is_bound:
#             for form in self.forms:
#                 if hasattr(form, 'nested'):
#                     result = result and form.nested.is_valid()

#         return result

#     def clean(self):
#         # If a parent form has no data, but its nested forms do, we should
#         # return an error, because we can't save the parent.
#         # For example, if the Product form is empty, but there are size and prices.

#         super().clean()

#         for form in self.forms:
#             if not hasattr(form, 'nested') or self._should_delete_form(form):
#                 continue

#             if self._is_adding_nested_inlines_to_empty_form(form):
#                 form.add_error(
#                     field=None,
#                     error=_('You are trying to add details to a product which '
#                             'does not yet exist. Please add information '
#                             'about the product and input the available sizes ' 
#                             'and its corresponding prices again.'))

#     def save(self, commit=True):
#         # Save the nested formsets.
#         result = super().save(commit=commit)

#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)

#         return result

# ProductDetailsFormset = inlineformset_factory(
#                         User, 
#                         Product, 
#                         formset=BaseProductFormset, 
#                         fields=('name', 'description', 'image_one', 'image_two', 'image_three',
#                         'stock', 'addon', 'instructions'),
#                         extra=1, 
#                     )

# class SizesForm(ModelForm):
#     class Meta:
#         model = Size
#         fields = ['name', 'price']

#         widgets = {
#             'name': forms.fields.TextInput(attrs={
#                 'class':'small-input default',
#                 'placeholder': 'Ex. 1 Dozen'}),
            
#             'price': forms.fields.TextInput(attrs={
#                 'class':'small-input default',
#                 'placeholder': 'Php'}),
#         }

#         labels = {
#             'name' : 'Available Sizes or Servings',
#             'price' : '',
#         }