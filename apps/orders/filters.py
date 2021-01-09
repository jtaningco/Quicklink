import django_filters
from django.db import models
from django import forms
from apps.orders.models import Order



class PendingOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [
            'product',
        ]
        labels = {
            'product' : '',
        }
        
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        super(PendingOrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['product'].label=''
        self.filters['product'].field.widget.attrs.update({
            'class':'select subtitle bold',
            'initial' : 'All Products',
        })
