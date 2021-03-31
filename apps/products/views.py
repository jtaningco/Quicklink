# from django.forms.models import inlineformset_factory
from apps.accounts.decorators import allowed_users, setup_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from django.views.generic import FormView
# from django.views.generic.detail import SingleObjectMixin
import json

from apps.products.models import *
from apps.accounts.models import User
from .forms import *
from django.db.models import Q

# Create your views here.
@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def products(request):
    user = request.user
    search_query = request.GET.get('search', '')

    if search_query:
        products = Product.objects.filter(Q(name__icontains=search_query) |
            Q(stock__icontains=search_query))
    else:
        products = Product.objects.filter(user=user)

    context = {'products':products}
    return render(request, 'products/products.html', context)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def productDetails(request, product_pk):
    product = Product.objects.get(id=product_pk)
    return render(request, 'products/product_modal.html', {'product':product})

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def addProduct(request):
    user = request.user
    form = ProductForm()
    imageFormset = ImageFormset()
    sizeFormset = SizeFormset()
    addonFormset = AddonFormset()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        
        if form.is_valid():        
            # Create product in database
            product = Product.objects.create(
                user=user,
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                orders=form.cleaned_data.get('orders'),
                instructions=form.cleaned_data.get('instructions'),
            )

            # Insert if radio is checked for stock
            if 'stocks-input-select' in request.POST:
                product.stock = form.cleaned_data.get('stock')
            else:
                product.stock = "Made to Order"

            # Insert if radio is checked for order
            if 'orders-input-select' in request.POST:
                product.orders = form.cleaned_data.get('orders')
            else:
                product.no_order_limit = True
            
            # Save Product
            product.save()

            imageFormset = ImageFormset(request.POST, instance=product)
            sizeFormset = SizeFormset(request.POST, instance=product)
            addonFormset = AddonFormset(request.POST, instance=product)
            
            # Save Formsets
            if imageFormset.is_valid():
                imageFormset.save()

            if sizeFormset.is_valid():
                sizeFormset.save()

            if addonFormset.is_valid():
                addonInputs = request.POST.get('addonForm-TOTAL_FORMS')
                if int(addonInputs) > 1:
                    addonFormset.save()
                    return redirect('/shop/products')
                elif int(addonInputs) == 1:
                    if request.POST.get('addon_set-0-addon') == '':
                        pass
                    else:
                        addonFormset.save()
                        return redirect('/shop/products')
                else:
                    return redirect('/shop/products')

    context = {'form':form, 'imageFormset':imageFormset, 'sizeFormset':sizeFormset, 'addonFormset':addonFormset}
    return render(request, 'products/product_form.html', context)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def updateProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    form = ProductForm(instance=product)

    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    sizeFormset = SizeFormset()
    addonFormset = AddonFormset()

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.description = form.cleaned_data.get('description')
            product.schedule = form.cleaned_data.get('schedule')
            product.days = form.cleaned_data.get('days')
            product.time = form.cleaned_data.get('time')
            product.instructions = form.cleaned_data.get('instructions')
            
            product.save()

            sizeFormset = SizeFormset(request.POST, instance=sizes)
            addonFormset = AddonFormset(request.POST, instance=addons)
            
            # Save Formsets
            if sizeFormset.is_valid():
                sizeFormset.save()

            if addonFormset.is_valid():
                addonInputs = request.POST.get('addonForm-TOTAL_FORMS')
                if int(addonInputs) > 1:
                    addonFormset.save()
                    return redirect('/shop/products')
                elif int(addonInputs) == 1:
                    if request.POST.get('addon_set-0-addon') == '':
                        pass
                    else:
                        addonFormset.save()
                        return redirect('/shop/products')
                else:
                    return redirect('/shop/products')

    context = {'form':form, 'product':product, 'sizeFormset':sizeFormset, 'addonFormset':addonFormset}
    return render(request, 'products/edit_product.html', context)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def deleteProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    if request.method == "POST":
        product.delete()
        return redirect('/shop/products/')

    context = {'product':product}
    return render(request, 'products/delete_product.html', context)