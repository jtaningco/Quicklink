from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.accounts.models import User, ShopInformation
from .forms import CustomerForm, MerchantForm, ShopInformationForm, ShopLogoForm, ShopBankAccount
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

            messages.success(request, 'Account successfully created')
            return redirect('accounts:merchant-login')
    context = {'form':form}
    return render(request, 'accounts/merchant-register.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def registerShopInformation(request):
    user = request.user
    form = ShopInformationForm()
    
    if request.method == 'POST':
        form = ShopInformationForm(request.POST)
        if form.is_valid():
            shop_info = ShopInformation.objects.create(
                user=user,
                shop_name=form.cleaned_data.get("shop_name"),
                shop_contact_number=form.cleaned_data.get("shop_contact_number"),
                shop_username=form.cleaned_data.get("shop_username"),
                shop_cod=form.cleaned_data.get("shop_cod"),
            )

            shop_info.shop_delivery_schedule.create(
                day_from=form.cleaned_data.get("day_from"),
                day_to=form.cleaned_data.get("day_to"),
                from_hour=form.cleaned_data.get("from_hour"),
                to_hour=form.cleaned_data.get("to_hour"),
            )
            
            shop_info.shop_address.create(
                line1=form.cleaned_data.get("line1"),
                line2=form.cleaned_data.get("line2"),
                city=form.cleaned_data.get("city"),
                province=form.cleaned_data.get("province"),
                postal_code=form.cleaned_data.get("postal_code"),
            )
            
            shop_info.shop_links.create(
                instagram=form.cleaned_data.get("instagram"),
                facebook=form.cleaned_data.get("facebook"),
                twitter=form.cleaned_data.get("twitter"),
            )

            shop_info.save()

            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:merchant-register-logo')

    context = {'form':form}
    return render(request, 'accounts/add-shop-information.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def registerShopLogo(request):
    user = request.user
    form = ShopLogoForm()

    if request.method == 'POST':
        form = ShopInformationForm(request.POST)
        if form.is_valid():
            shop_info = ShopInformation.objects.get(user=user)
            shop_info.shop_logo.create(
                logo=form.cleaned_data.get("logo")
            )
            shop_info.save()

            messages.success(request, 'Logo successfully updated')
            return redirect('accounts:merchant-register-payment')

    context = {'form':form}
    return render(request, 'accounts/add-shop-logo.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_role=User.Types.MERCHANT)
def registerShopAccount(request):
    user = request.user
    form = ShopBankAccount()

    if request.method == 'POST':
        form = ShopBankAccount(request.POST)
        if form.is_valid():
            shop_info = ShopInformation.objects.get(user=user)
            shop_info.shop_account.create(
                bank_account=form.cleaned_data.get("bank_account"),
                cardholder_name=form.cleaned_data.get("cardholder_name"),
                account_number=form.cleaned_data.get("account_number")
            )
            shop_info.save()

            messages.success(request, 'Bank account details successfully updated')
            return redirect('products:products')

    context = {'form':form}
    return render(request, 'accounts/add-shop-account.html', context)

@unauthenticated_merchant
def loginMerchant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not hasattr(user, 'info_shop'):
                return redirect('accounts:merchant-register-shop')
            else:
                return redirect('products:products')
        else:
            messages.info(request, "email or password is incorrect.")
    
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
