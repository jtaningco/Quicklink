import django_filters as filters
from django.db import models
from django import forms

from apps.products.models import Product
from apps.orders.models import ProductOrder
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
        ]
        labels = {
            'product': '',
        }

    # Filter product owners to only those that are owned by the logged-in user
    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        return parent.filter(order__shop=user) \
            | parent.filter(order__order_status="Pending")
        
    def __init__(self, data=None, queryset=None, request=None, prefix=None):
        # Initialize Filter
        super(PendingOrderFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['product'].label=''
        self.filters['product'].field.widget.attrs.update({
            'class':'select subtitle bold',
        })
        self.filters['product'].initial = super().qs[1]
