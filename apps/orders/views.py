from django.shortcuts import render, redirect
from apps.products.models import Product, Size, Addon
from apps.orders.models import Order
from .forms import OrderForm
from .filters import PendingOrderFilter
from django.utils.timezone import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import allowed_users
from apps.accounts.models import User

# Create your views here.
@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def pendingOrders(request):
    orders = Order.objects.filter(order_status="Pending")
    orderCount = Order.objects.filter(order_status="Pending").count()

    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter, 'orderCount':orderCount}
    return render(request, 'orders/pending_orders.html', context)

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

@login_required(login_url='accounts:login')
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

@login_required(login_url='accounts:login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def viewProducts(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'orders/available_products.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def addOrder(request, pk):
    product = Product.objects.get(id=pk)
    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    form = OrderForm(initial={'product': product})
    if request.method == 'POST':
        form = OrderForm(request.POST)
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

@login_required(login_url='accounts:login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def deleteOrder(request, order_pk):
    order = Order.objects.get(id=order_pk)
    if request.method == "POST":
        order.delete()
        return redirect('/shop/orders/')

    context = {'order':order}
    return render(request, 'orders/delete_order.html', context)