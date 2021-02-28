from django.shortcuts import render, redirect
from apps.products.models import Product, Size, Addon
from apps.orders.models import Order, ProductOrder
from .forms import PreviewOrderForm, OrderForm
from .filters import PendingOrderFilter
from django.utils.timezone import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import allowed_users
from apps.accounts.models import *

from django.http import HttpResponse

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
    # RESTART THIS TOMORROW
    
    user = request.user
    product = Product.objects.filter(user=user).order_by('name')[0]

    orders = Order.objects.filter(shop=user, order_status="Pending")
    productOrders = ProductOrder.objects.filter(order__in=orders).order_by('product')

    orderCount = ProductOrder.objects.filter(order__in=orders).count()

    productFilter = PendingOrderFilter(request.GET, queryset=productOrders)
    products = productFilter.qs.filter(order__order_status="Pending")
    
    context = {'orders':orders, 'products':productOrders, 'productFilter':productFilter, 'orderCount':orderCount}
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
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.MERCHANT, User.Types.ADMIN])
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
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.MERCHANT, User.Types.ADMIN])
def viewProducts(request, shop_pk):
    shop = ShopInformation.objects.get(id=shop_pk)
    products = Product.objects.filter(user=shop.user)
    sizes = Size.objects.filter(product__in=products)

    size_prices = []

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
    context = {'products':products, 'shop':shop, 'links':links, 'address':address, 'sizes':sizes}
    return render(request, 'customers/products.html', context)

# Add Products to Cart (Customers)
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.MERCHANT, User.Types.ADMIN])
def addOrder(request, shop_pk, product_pk):
    user = request.user
    shop = ShopInformation.objects.get(id=shop_pk)
    shopOwner = shop.user

    product = Product.objects.get(id=product_pk)

    # sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    
    try:
        order = Order.objects.get(user=user, shop=shopOwner)
        print("ORDER Successfully found! \n")
    except:
        order = Order.objects.create(
            user=user,
            shop=shopOwner,
        )
        order.save()
        print("ORDER Successfully created! \n")
    
    form = OrderForm(product=product, initial={
        'product': product, 'order': order
    })

    if request.method == 'POST':
        print("POST Success! \n")
        # Check if order form exists        
        
        form = OrderForm(request.POST, product=product)
        print("Form response successfully loaded! \n")

        # Save form if form is valid
        if form.is_valid():
            print("Form is valid! \n")
            form.save()

            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
                product.save()
            
            return HttpResponse('Order successfully created!')
        else:
            form = OrderForm(data=request.POST)
            print(form.errors.as_data())
            return HttpResponse('Order failed!')

    # 'sizes':sizes, 
    context = {'form':form, 'product':product, 'addons':addons}
    return render(request, 'customers/order_form.html', context)