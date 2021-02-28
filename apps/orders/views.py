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
    search_query = request.GET.get('search', '')

    if search_query:
        orders = Order.objects.filter(Q(order_status__icontains=search_query) |
            Q(payment_status__icontains=search_query) |
            Q(order_date__icontains=search_query) |
            Q(delivery_date__icontains=search_query) |
            Q(id__icontains=search_query))
    else:
        orders = Order.objects.all()

    context = {'orders':orders }
    return render(request, 'orders/order_summary.html', context)

# Pending Orders
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def pendingOrders(request):
    orders = Order.objects.filter(order_status="Pending")
    orderCount = Order.objects.filter(order_status="Pending").count()

    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter, 'orderCount':orderCount}
    return render(request, 'orders/pending_orders.html', context)

# Pending Orders with Today's Filter
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def pendingToday(request):
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(hours=24)
    orders = Order.objects.filter(order_status="Pending", 
            delivery_date__range=(today, tomorrow))
    
    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter}
    return render(request, 'orders/pending_orders_today.html', context)

# Pending Orders with Next Seven Days Filter
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def pendingNextSevenDays(request):
    today = datetime.today()
    next_seven_days = datetime.today() + timedelta(days=7)
    orders = Order.objects.filter(order_status="Pending",
            delivery_date__range=(today, next_seven_days))
    
    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter}
    return render(request, 'orders/pending_orders_week.html', context)

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
    shops = ShopInformation.objects.all()
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
def addOrder(request, product_pk):
    user = request.user
    product = Product.objects.get(id=product_pk)
    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    form = OrderForm(product=product)
    if request.POST == 'POST':
        # Check if order form exists
        try:
            order = Order.objects.get(user=user)
        except:
            order = Order.objects.create(
                user=user
            )
            order.save()
        form = OrderForm(product=product, data=request.POST)
        
        # Save form if form is valid
        if form.is_valid():
            form.order = order
            form.save()

            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
                product.save()
            
            return HttpResponse('Order successfully created!')
        else:
            form = OrderForm(request.POST)
            print(form.errors.as_data())

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons}
    return render(request, 'customers/order_form.html', context)