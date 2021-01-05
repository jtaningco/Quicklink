from django.shortcuts import render
from django.http import HttpResponse

from apps.products.models import Product, Tag

# Create your views here.
def products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products':products})

def addProduct(request):
    context = {}
    return render(request, 'products/product_form.html', context)