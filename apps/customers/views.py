from django.shortcuts import render, redirect
from django.utils.timezone import datetime, timedelta

from apps.products.models import Product, Size, Addon
from apps.orders.models import Order, ProductOrder
from apps.accounts.models import *

from apps.orders.forms import OrderForm, CheckoutForm

from django.http import JsonResponse
from decimal import Decimal
import json

# Create your views here.
# View Products (Customers)
def viewShops(request):
    users = User.objects.filter(role=User.Types.MERCHANT)
    allShops = ShopInformation.objects.all()
    shops = []

    for shop in allShops:
        if shop.user in users:
            shops.append(shop)

    context = {'shops':shops}
    return render(request, 'customers/shops.html', context)

# View Products (Customers)
def viewProducts(request, shop_pk):
    shop = ShopInformation.objects.get(id=shop_pk)
    user = shop.user
    products = Product.objects.filter(user=shop.user)
    sizes = Size.objects.filter(product__in=products)

    size_prices = []

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
        print([item for item in items.all()])
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    for product in products:
        for size in sizes:
            if size.product == product:
                size_prices.append(size.price_size)
            else:
                continue
        product.min_price = min(size_prices)
        product.max_price = max(size_prices)
        product.save()
        size_prices.clear()

    context = {'products':products, 'shop':shop, 'user':user, 'sizes':sizes, 'items':items, 'order':order, 'shop':shop}
    return render(request, 'customers/products.html', context)

# Add Products to Cart (Customers)
def addOrder(request, shop_pk, product_pk):
    user = request.user
    shop = ShopInformation.objects.get(id=shop_pk)
    shopOwner = shop.user

    product = Product.objects.get(id=product_pk)

    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, shop=shopOwner, complete=False)
        items = order.productorder_set.all()
        form = OrderForm(initial={
            'product': product, 'order': order
        })
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        form = OrderForm(initial={
            'product': product
        })

    if request.method == 'POST':
        # Check if order form exists        
        form = OrderForm(request.POST, product=product)

        # Save form if form is valid
        if form.is_valid():
            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
                product.save()
            return redirect('add/')
        else:
            form = OrderForm(data=request.POST)
            print(form.errors.as_data())
            return HttpResponse('Order failed!')

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons, 'shop':shop, 'order':order}
    return render(request, 'customers/order_form.html', context)

def addItem(request, shop_pk, product_pk):
    data = json.loads(request.body)
    form = data['form']
    shopId = data['shopId']
    productId = data['productId']
    action = data['action']

    addons_list = []
    quantity = 1

    for i in form:
        if i.get('name') == 'size':
            size = Size.objects.get(id=i.get('value'))
        
        if i.get('name') == 'addons':
            addons_list.append(i.get('value'))
        
        if i.get('name') == 'instructions':
            instructions = i.get('value')
        
        if i.get('name') == 'quantity':
            quantity = int(i.get('value'))
    
    addons = Addon.objects.filter(id__in=addons_list)

    customer = request.user
    shop = ShopInformation.objects.get(id=shopId)
    shopOwner = shop.user

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, shop=shopOwner, complete=False)

    if addons:
        addons_total = 0
        for i in addons:
            addons_total += (quantity * i.price_addon)
        total = (quantity * size.price_size) + addons_total
    else:    
        total = (quantity * size.price_size)

    productOrder, created = ProductOrder.objects.get_or_create(
        order=order, product=product, size=size, addons__in=addons,
        instructions=instructions, quantity=quantity, total=total)

    for addon in addons:
        productOrder.addons.add(addon)

    productOrder.save()
    
    order.subtotal = 0
    for product in order.productorder_set.all():
        order.subtotal += product.total

    order.fees = order.subtotal * Decimal(0.05)
    order.total = order.subtotal + order.fees
    order.save()

    return redirect('/shops/')

def updateItem(request, shop_pk, product_pk):
    data = json.loads(request.body)
    shopId = data['shopId']
    itemId = data['itemId']
    productId = data['productId']
    action = data['action']

    productOrder = ProductOrder.objects.get(id=itemId)
    order = productOrder.order
    addons = productOrder.addons.all()

    if action == "increase":
        productOrder.quantity = (productOrder.quantity + 1)
    elif action == "decrease":
        productOrder.quantity = (productOrder.quantity - 1)

    if addons:
        addons_total = 0
        for i in addons:
            addons_total += (productOrder.quantity * i.price_addon)
        productOrder.total = (productOrder.quantity * productOrder.size.price_size) + addons_total
    else:    
        productOrder.total = (productOrder.quantity * productOrder.size.price_size)

    productOrder.save()

    if productOrder.quantity <= 0:
        productOrder.delete()
    
    order.subtotal = 0
    for product in order.productorder_set.all():
        order.subtotal += product.total

    order.fees = order.subtotal * Decimal(0.05)
    order.total = order.subtotal + order.fees
    order.save()

    return JsonResponse('Item was edited', safe=False)

def checkout(request, shop_pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    form = CheckoutForm()

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            sessionSender = CustomerInformation.objects.create(
                customer_name = form.cleaned_data.get('name'),
                customer_email = form.cleaned_data.get('email'),
                customer_contact_number = form.cleaned_data.get('contact_number')
            )
            sessionSender.save()

            sessionAddress = Address.objects.create(
                line1 = form.cleaned_data.get('line1'),
                line2 = form.cleaned_data.get('line2'),
                city = form.cleaned_data.get('city'),
                province = form.cleaned_data.get('province'),
                postal_code = form.cleaned_data.get('postal_code'),
            )
            sessionAddress.save()

            orderNotifications = Notification.objects.create(
                sms = form.cleaned_data.get('sms'),
                email = form.cleaned_data.get('email')
            )
            orderNotifications.save()

            orderInfo = OrderInformation.objects.create(
                order = order,
                session_sender = sessionSender,
                session_address = sessionAddress,
                session_notification = orderNotifications,
            )
            orderInfo.save()

            bankAccount = form.cleaned_data.get('bank_name')

            # If Debit/Credit
            if bankAccount == CheckoutForm.BANKS[0]:
                return HttpResponse("Pay with Debit/Credit!")
            
            # If eWallet
            elif bankAccount == CheckoutForm.BANKS[1]:
                return HttpResponse("Pay with eWallet!")

            # if COD
            else:
                return HttpResponse("Pay with COD!")

    context = {'items':items, 'order':order}
    return render(request, 'customers/checkout.html', context)