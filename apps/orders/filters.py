import django_filters as filters
from django.db import models
from django import forms

from apps.products.models import Product
from apps.orders.models import Order, ProductOrder
from django.utils.translation import gettext as _

def productChoices(request):
    if request is None:
        return Product.objects.none()

    user = request.user
    return Product.objects.filter(user=user).order_by('name')

class PendingOrderFilter(filters.FilterSet):
    product = filters.ModelChoiceFilter(queryset=productChoices, empty_label=_("Select Product"))
    class Meta:
        model = ProductOrder
        fields = [
            'product', 
            'delivery_date',
        ]
        labels = {
            'product': '',
            'delivery_date': '',
        }

    # Filter product owners to only those that are owned by the logged-in user
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        return parent.filter(order__shop=user) \
            | parent.filter(order__order_status="Pending")

    @property
    def get_product(self):
        return self.data['product']
        
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        # Initialize Filter
        super(PendingOrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['product'].label=''
        self.filters['product'].field.widget.attrs.update({
            'class':'subtitle bold',
        })
        self.filters['delivery_date'].label=''
        self.filters['delivery_date'].field.widget.attrs.update({
            'class':'date-input-content subtitle',
        })

class OrderFilter(filters.FilterSet):
    delivery_date = filters.DateFilter()
    class Meta:
        model = Order
        fields = [
            'delivery_date',
        ]
        labels = {
            'delivery_date': '',
        }

    # Filter product owners to only those that are owned by the logged-in user
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        return parent.filter(shop=user)
        
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        # Initialize Filter
        super(OrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['delivery_date'].label=''
        self.filters['delivery_date'].field.widget.attrs.update({
            'class':'date-input-content subtitle',
        })
