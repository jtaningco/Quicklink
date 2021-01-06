from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context, loader

from apps.products.models import Product
from .forms import ProductForm

# Create your views here.
def home(request):
    template = loader.get_template('quicklink/base.html')
    return HttpResponse(template.render())

def products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products':products})

def productDetails(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'products/product_modal.html', {'product':product})

def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('products/products.html')

    context = {'form':form}
    return render(request, 'products/product_form.html', context)

def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            redirect('products/products.html')

    context = {'form':form}
    return render(request, 'products/product_form.html', context)