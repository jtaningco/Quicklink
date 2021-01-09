# from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib import messages

# from django.views.generic import FormView
# from django.views.generic.detail import SingleObjectMixin

from apps.products.models import Product
from apps.accounts.models import User
from .forms import ProductForm

# Create your views here.
def products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products':products})

def productDetails(request, product_pk):
    product = Product.objects.get(id=product_pk)
    return render(request, 'products/product_modal.html', {'product':product})

def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print('PRINTING POST: ', request.POST)
            form.save()
            return redirect('/shop/products')

    context = {'form':form}
    return render(request, 'products/product_form.html', context)

def updateProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            redirect('products/products.html')

    context = {'form':form}
    return render(request, 'products/product_form.html', context)
