from django.shortcuts import render, redirect
from django.utils.timezone import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .forms import PreviewOrderForm, OrderForm
from .filters import PendingOrderFilter
from apps.products.models import Product, Size, Addon
from apps.orders.models import Order, ProductOrder
from apps.accounts.decorators import allowed_users
from apps.accounts.models import *

from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import json

# Create your views here.

# Order Summary
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def orders(request):
    user = request.user
    search_query = request.GET.get('search', '')

    if search_query:
        orders = Order.objects.filter(shop=user | 
            Q(order_status__icontains=search_query) |
            Q(payment_status__icontains=search_query) |
            Q(order_date__icontains=search_query) |
            Q(delivery_date__icontains=search_query) |
            Q(id__icontains=search_query))
    else:
        orders = Order.objects.filter(shop=user)

    context = {'orders':orders }
    return render(request, 'orders/order_summary.html', context)

# Pending Orders
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def pendingOrders(request):
    # Get merchant user
    user = request.user

    # Get initial value for filter set (Alphabetical Order)
    productChoices = Product.objects.filter(user=user).order_by('name')
    product = productChoices[0]

    # Get pending orders
    orders = Order.objects.filter(shop=user, order_status="Pending")
    
    # Get pending product orders
    productOrders = ProductOrder.objects.filter(order__in=orders).order_by('product')

    # Get total count of orders that are in pending orders Query set
    orderCount = ProductOrder.objects.filter(order__in=orders).count()

    # Product filter form
    productFilter = PendingOrderFilter(request.GET, request=request, queryset=productOrders)
    products = productFilter.qs
    
    try:
        addons = Addon.objects.filter(product=products[0].product)
        selected_addons = []
        for product in products:
            for addon in product.addons.all():
                if addon in addons: selected_addons.append(addon)
        orderCount = products.count()
    except:
        addons = Addon.objects.filter(product=product)
        selected_addons = []
        for product in productOrders:
            for addon in product.addons.all():
                if addon in addons: selected_addons.append(addon.addon)
        orderCount = productOrders.count()
    
    context = {'orders':orders, 
    'products':products,
    'productOrders':productOrders, 
    'products_verification':list(products),
    'productOrders_verification':list(productOrders), 
    'productFilter':productFilter, 
    'orderCount':orderCount, 
    'addons':addons, 
    'selected_addons':selected_addons}
    return render(request, 'orders/pending_orders.html', context)

# View Products (Merchant Preview)
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def menuPreview(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'orders/available_products.html', context)

# Order Form (Merchant Preview)
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def addPreviewOrder(request, pk):
    product = Product.objects.get(id=pk)
    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    form = PreviewOrderForm(initial={'product': product})
    if request.method == 'POST':
        form = PreviewOrderForm(request.POST)
        if form.is_valid():
            alert("The form has been submitted, but the data won't be portrayed in your merchant dashboard for this is merely a test.")
            return redirect('/shop/orders/')

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons}
    return render(request, 'orders/order_form.html', context)

# Deleting Orders (For Testing)
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def deleteOrder(request, order_pk):
    order = Order.objects.get(id=order_pk)
    if request.method == "POST":
        order.delete()
        return redirect('/shop/orders/')

    context = {'order':order}
    return render(request, 'orders/delete_order.html', context)

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

    address = Address.objects.get(user=shop.user)
    links = SocialMediaLink.objects.get(user=shop.user)
    context = {'products':products, 'shop':shop, 'links':links, 'address':address, 'sizes':sizes, 'items':items, 'order':order, 'shop':shop}
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
        form = OrderForm(product=product, initial={
            'product': product, 'order': order
        })
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        form = OrderForm(product=product, initial={
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

def checkout(request, shop_pk):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items':items, 'order':order}
    return render(request, 'customers/checkout.html', context)

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

    return JsonResponse('Item was added', safe=False)

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

    return JsonResponse('Item was added', safe=False)