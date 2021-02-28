import django_filters
from django_filters import CharFilter
from django.db import models
from django import forms
from apps.orders.models import ProductOrder

class PendingOrderFilter(django_filters.FilterSet):
    class Meta:
        model = ProductOrder
        fields = [
            'product',
        ]
        labels = {
            'product' : '',
        }
        
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        super(PendingOrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)

        # Initialize Filter
        data = data.copy()
        if len(data) == 0:
            data['product'] = queryset[0]

        self.filters['product'].label=''
        self.filters['product'].field.widget.attrs.update({
            'class':'select subtitle bold',
        })
        self.filters['product'].initial = queryset[0]
