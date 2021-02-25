# from django.forms.models import inlineformset_factory
from apps.accounts.decorators import allowed_users
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from django.views.generic import FormView
# from django.views.generic.detail import SingleObjectMixin

from apps.products.models import *
from apps.accounts.models import User
from .forms import *
from django.db.models import Q

# Create your views here.
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
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

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def productDetails(request, product_pk):
    product = Product.objects.get(id=product_pk)
    return render(request, 'products/product_modal.html', {'product':product})

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def addProduct(request):
    user = request.user
    form = ProductForm()
    sizeFormset = SizeFormset()
    addonFormset = AddonFormset()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        sizeFormset = SizeFormset(request.POST)
        addonFormset = AddonFormset(request.POST)

        if form.is_valid():
            product = Product.objects.create(
                user=user,
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                days=form.cleaned_data.get('days'),
                week=form.cleaned_data.get('week'),
                image=form.cleaned_data.get('image'),
                instructions=form.cleaned_data.get('instructions'),
            )

            # Insert if radio is checked for stock
            if 'made-to-order' in request.POST:
                product.stock = "Made to Order"
            elif 'stocks-input-select' in request.POST:
                product.stock = form.cleaned_data.get('stock')

            # Insert if radio is checked for order
            if 'no-order-limits' in request.POST:
                product.orders = "No Limit"
            elif 'orders-input-select' in request.POST:
                product.orders = form.cleaned_data.get('orders')
            
            # Save Product
            product.save()
            return redirect('/shop/products')

            # Save Formsets
            if sizeFormset.is_valid() and addonFormset.is_valid():
                for sizeForm in sizeFormset:
                    size = Size.objects.create(
                        product=product,
                        size=sizeForm.cleaned_data.get('size'),
                        price_size=sizeForm.cleaned_data.get('price_size')
                    )
                    size.save()

                    addonInputs = form.cleaned_data.get('addonForm-TOTAL_FORMS')
                    if int(addonInputs) >= 1:
                        for addonForm in addonFormset:
                            addon = Addon.objects.create(
                                product=product,
                                addon=addonForm.cleaned_data.get('addon'),
                                price_addon=addonForm.cleaned_data.get('price_addon')
                            )
                            addon.save()
                            return redirect('/shop/products')
                    else:
                            return redirect('/shop/products')

    context = {'form':form, 'sizeFormset':sizeFormset, 'addonFormset':addonFormset}
    return render(request, 'products/product_form.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def updateProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/shop/products')

    context = {'form':form, 'product':product}
    return render(request, 'products/edit_product.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def deleteProduct(request, product_pk):
    product = Product.objects.get(id=product_pk)
    if request.method == "POST":
        product.delete()
        return redirect('/shop/products/')

    context = {'product':product}
    return render(request, 'products/delete_product.html', context)