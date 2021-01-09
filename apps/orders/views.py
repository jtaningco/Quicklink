from django.shortcuts import render, redirect
from apps.products.models import Product
from apps.orders.models import Order
from .forms import OrderForm
from .filters import PendingOrderFilter
from django.utils.timezone import datetime, timedelta

# Create your views here.
def orders(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_summary.html', {'orders':orders})

def pendingOrders(request):
    orders = Order.objects.filter(order_status="Pending")
    orderCount = Order.objects.filter(order_status="Pending").count()

    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter, 'orderCount':orderCount}
    return render(request, 'orders/pending_orders.html', context)

def pendingToday(request):
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(hours=24)
    orders = Order.objects.filter(order_status="Pending", 
            delivery_date__range=(today, tomorrow))
    
    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter}
    return render(request, 'orders/pending_orders_today.html', context)

def pendingNextSevenDays(request):
    today = datetime.today()
    next_seven_days = datetime.today() + timedelta(days=7)
    orders = Order.objects.filter(order_status="Pending",
            delivery_date__range=(today, next_seven_days))
    
    productFilter = PendingOrderFilter(request.GET, queryset=orders)
    orders = productFilter.qs.filter(order_status="Pending")
    
    context = {'orders':orders, 'productFilter':productFilter}
    return render(request, 'orders/pending_orders_week.html', context)

def viewProducts(request):
    products = Product.objects.all()
    return render(request, 'orders/available_products.html', {'products':products})

def addOrder(request, pk):
    product = Product.objects.get(id=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form, 'product':product}
    return render(request, 'orders/order_form.html', context)