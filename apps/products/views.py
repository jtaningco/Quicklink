# from django.forms.models import inlineformset_factory
from apps.accounts.decorators import allowed_users, setup_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
        products = Product.objects.filter(Q(user=user) & 
            Q(name__icontains=search_query) |
            Q(stock__icontains=search_query)
        )
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
                instructions=form.cleaned_data.get('instructions'),
            )

            # Insert if radio is checked for stock
            if 'stocks-input-select' in request.POST:
                product.stock = form.cleaned_data.get('stock')
                product.made_to_order = False
            else:
                product.made_to_order = True
                product.stock = 0

            # Insert if radio is checked for order
            if 'orders-input-select' in request.POST:
                product.orders = form.cleaned_data.get('orders')
                product.no_order_limit = False
            else:
                product.no_order_limit = True
                product.orders = 0
            
            # Save Product
            product.save()

            imageFormset = ImageFormset(request.POST, request.FILES, instance=product)
            sizeFormset = SizeFormset(request.POST, instance=product)
            addonFormset = AddonFormset(request.POST, instance=product)
            
            # Save Formsets
            if imageFormset.is_valid():
                imageFormset.save()
                images = Image.objects.filter(product=product)
                count = 0
                for image in images:
                    name = image.get_product_name
                    image.name = name
                    image.save()

            if sizeFormset.is_valid():
                sizeFormset.save()

            if addonFormset.is_valid():                
                addonInputs = request.POST.get('addonForm-TOTAL_FORMS')
                if int(addonInputs) > 1:
                    addonFormset.save()
                    return redirect('/shop/products/')
                elif int(addonInputs) == 1:
                    if request.POST.get('addon_set-0-addon') == '':
                        pass
                    else:
                        addonFormset.save()
                        return redirect('/shop/products/')
                else:
                    return redirect('/shop/products/')

    context = {'form':form, 'imageFormset':imageFormset, 'sizeFormset':sizeFormset, 'addonFormset':addonFormset}
    return render(request, 'products/product_form.html', context)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def updateProduct(request, product_pk):
    user = request.user
    product = Product.objects.get(id=product_pk)
    form = ProductForm(instance=product)
    images = list(Image.objects.filter(product=product))

    imageFormset = ImageFormset(instance=product)
    sizeFormset = SizeFormset(instance=product)
    addonFormset = AddonFormset(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product.name = form.cleaned_data.get('name')
            product.description = form.cleaned_data.get('description')
            product.instructions = form.cleaned_data.get('instructions')

            # Insert if radio is checked for stock
            if 'stocks-input-select' in request.POST:
                product.stock = form.cleaned_data.get('stock')
                product.made_to_order = False
            else:
                product.made_to_order = True
                product.stock = 0

            # Insert if radio is checked for order
            if 'orders-input-select' in request.POST:
                product.orders = form.cleaned_data.get('orders')
                product.no_order_limit = False
            else:
                product.no_order_limit = True
                product.orders = 0
            
            # Save Product
            product.save()

            imageFormset = ImageFormset(request.POST, request.FILES, instance=product)
            sizeFormset = SizeFormset(request.POST, instance=product)
            addonFormset = AddonFormset(request.POST, instance=product)
            
            # Save Formsets
            if sizeFormset.is_valid():
                sizeFormset.save()

            if addonFormset.is_valid():
                addonInputs = request.POST.get('addonForm-TOTAL_FORMS')
                if int(addonInputs) > 1:
                    addonFormset.save()
                    return redirect('/shop/products/')
                elif int(addonInputs) == 1:
                    if request.POST.get('addon_set-0-addon') == '':
                        pass
                    else:
                        addonFormset.save()
                else: pass

            if imageFormset.is_valid():
                imageFormset.save()
                new_images = Image.objects.filter(product=product)
                for image in new_images:
                    name = image.get_product_name
                    image.name = name
                    image.save()
                return redirect('/shop/products/')
            else:
                return redirect('/shop/products/')

    context = {'form':form, 'product':product, 'images':images, 'imageFormset':imageFormset, 'sizeFormset':sizeFormset, 'addonFormset':addonFormset}
    return render(request, 'products/edit_product.html', context)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def setProductsAsActive(request):
    if request.method == "POST" and request.is_ajax:
        productId = request.POST.get('products')
        product = Product.objects.get(pk=productId)
        product.active = True
        product.save()
        return redirect('/shop/products/')
    return JsonResponse(request.POST, safe=False)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def setProductsAsInactive(request):
    if request.method == "POST" and request.is_ajax:
        productsList = json.loads(request.POST.get('products'))
        for productId in productsList:
            product = Product.objects.get(pk=productId)
            product.active = False
            product.save()
        return redirect('/shop/products/')
    return JsonResponse(request.POST, safe=False)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def deleteSelectedProducts(request):
    if request.method == "POST" and request.is_ajax:
        productsList = json.loads(request.POST.get('products'))
        for productId in productsList:
            product = Product.objects.get(pk=productId)
            product.delete()
        return redirect('/shop/products/')
    return JsonResponse(request.POST, safe=False)

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def duplicateProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    product.id = None
    product.save()
    return redirect('/shop/products/')

@login_required(login_url='accounts:login')
@setup_required
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def deleteProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    product.delete()
    return redirect('/shop/products/')