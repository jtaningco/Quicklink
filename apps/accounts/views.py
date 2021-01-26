from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from apps.accounts.models import User
from .forms import CustomerForm, MerchantForm
from .decorators import allowed_users, unauthenticated_customer, unauthenticated_merchant

# Create your views here.
@unauthenticated_merchant
def registerMerchant(request):
    form = MerchantForm(initial={'role': User.Types.MERCHANT})
    
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                role=form.cleaned_data.get("role"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created for ' + username)
            return redirect('accounts:merchant-login')

    context = {'form':form}
    return render(request, 'accounts/merchant-register.html', context)

@unauthenticated_merchant
def loginMerchant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('products:products')
        else:
            messages.info(request, "Username or password is incorrect.")
    
    context = {}
    return render(request, 'accounts/merchant-login.html', context)

def logoutMerchant(request):
    logout(request)
    return redirect('accounts:merchant-login')

@unauthenticated_customer
def registerCustomer(request):
    form = CustomerForm(initial={'role': User.Types.CUSTOMER})
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                role=form.cleaned_data.get("role"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created for ' + username)
            return redirect('accounts:customer-login')

    context = {'form':form}
    return render(request, 'accounts/customer-register.html', context)

@unauthenticated_customer
def loginCustomer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:customer-landing')
        else:
            messages.info(request, "Username or password is incorrect.")
    
    context = {}
    return render(request, 'accounts/customer-login.html', context)

def logoutCustomer(request):
    logout(request)
    return redirect('accounts:customer-login')

@allowed_users(allowed_role=User.Types.CUSTOMER)
def landingCustomer(request):
    context = {}
    return render(request, 'accounts/sample-customer-landing.html', context)
