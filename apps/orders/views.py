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

# Create your views here.

# Order Summary
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
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
@allowed_users(allowed_role=User.Types.MERCHANT)
def pendingOrders(request):
    orders = Order.objects.filter(order_status="Pending")
    orderCount = Order.objects.filter(order_status="Pending").count()

    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter, 'orderCount':orderCount}
    return render(request, 'orders/pending_orders.html', context)

# Pending Orders with Today's Filter
@login_required(login_url='accounts:login')
@allowed_users(allowed_role=User.Types.MERCHANT)
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
@allowed_users(allowed_role=User.Types.MERCHANT)
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
@allowed_users(allowed_role=User.Types.MERCHANT)
def menuPreview(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'orders/available_products.html', context)

# Order Form (Merchant Preview)
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def addPreviewOrder(request, pk):
    product = Product.objects.get(id=pk)
    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    form = PreviewOrderForm(initial={'product': product})
    if request.method == 'POST':
        form = PreviewOrderForm(request.POST)
        if form.is_valid():
            form.save()
            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
            return redirect('/shop/orders/')

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons}
    return render(request, 'orders/order_form.html', context)

# Deleting Orders (For Testing)
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def deleteOrder(request, order_pk):
    order = Order.objects.get(id=order_pk)
    if request.method == "POST":
        order.delete()
        return redirect('/shop/orders/')

    context = {'order':order}
    return render(request, 'orders/delete_order.html', context)

# View Products (Customers)
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_role=User.Types.CUSTOMER)
def viewShops(request):
    shops = ShopInformation.objects.all()
    context = {'shops':shops}
    return render(request, 'customers/shops.html', context)

# View Products (Customers)
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_role=User.Types.CUSTOMER)
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
        print(product)
        size_prices.clear()

    address = Address.objects.get(user=shop.user)
    links = SocialMediaLink.objects.get(user=shop.user)
    context = {'products':products, 'shop':shop, 'links':links, 'address':address, 'sizes':sizes}
    return render(request, 'customers/products.html', context)

# Add Products to Cart (Customers)
@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_role=User.Types.CUSTOMER)
def addOrder(request, product_pk):
    user = request.user
    order = Order.objects.get(user=user)
    product = Product.objects.get(id=product_pk)
    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    form = OrderForm()
    if request.method == 'POST':
        # Check if order form exists
        if not order:
            order = Order.objects.create(
                user=user
            )
            order.save()

        if form.is_valid():
            orderForm = ProductOrder.objects.create(
                order=order,
                product=product,
                size=form.cleaned_data.get('size'),
                addons=form.cleaned_data.get('addons'),
                quantity=form.cleaned_data.get('quantity'),
                instructions=form.cleaned_data.get('instructions')
            )
            orderForm.save()
            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
            return redirect('/shop/orders/shops')

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons}
    return render(request, 'customers/order_form.html', context)