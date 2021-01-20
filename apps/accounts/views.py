from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from apps.accounts.models import User
from .forms import CustomerForm, MerchantForm
from .decorators import merchants_only, unauthenticated_user

# Create your views here.
@unauthenticated_user
def registerMerchant(request):
    if request.user.is_authenticated:
        return redirect('products:products')
    else:
        form = MerchantForm(initial={'role': User.Types.MERCHANT,})
    
        if request.method == 'POST':
            form = MerchantForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account successfully created for ' + user)
                return redirect('accounts:merchant-login')

        context = {'form':form}
        return render(request, 'accounts/merchant-register.html', context)

@unauthenticated_user
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

@unauthenticated_user
def registerCustomer(request):
    if request.user.is_authenticated:
        return HttpResponse('You are logged in as a Customer.')
    else:
        form = CustomerForm()
        if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account successfully created for ' + user)
                return redirect('accounts:customer-login')

        context = {'form':form}
        return render(request, 'accounts/customer-register.html', context)

@unauthenticated_user
def loginCustomer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'CUSTOMER':
                return redirect('accounts:customer-landing')
        else:
            messages.info(request, "Username or password is incorrect.")
    
    context = {}
    return render(request, 'accounts/merchant-login.html', context)

def logoutCustomer(request):
    logout(request)
    return redirect('accounts:customer-login')

@unauthenticated_user
def landingCustomer(request):
    context = {}
    return render(request, 'accounts/sample-customer-landing.html', context)
