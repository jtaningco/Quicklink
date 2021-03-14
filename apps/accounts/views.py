from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.accounts.models import *
from .forms import *
from .decorators import allowed_users, unauthenticated_customer, unauthenticated_merchant

# XenPlatform Account Creation
from xendit import Xendit, XenPlatformAccountType, XenPlatformURLType

# Create your views here.
@unauthenticated_merchant
def registerMerchant(request):
    form = MerchantForm(initial={'role': User.Types.MERCHANT})
    
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                role=User.Types.MERCHANT,
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()

            messages.success(request, 'Account successfully created')
            return redirect('accounts:merchant-login')
    context = {'form':form}
    return render(request, 'accounts/merchant-register.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
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
            shop_info.save()
            
            open_hours = OpenHours.objects.create(
                shop=shop_info,
                day_from=form.cleaned_data.get("day_from"),
                day_to=form.cleaned_data.get("day_to"),
                from_hour=form.cleaned_data.get("from_hour"),
                to_hour=form.cleaned_data.get("to_hour"),
            )
            
            shop_address = Address.objects.create(
                user=user,
                line1=form.cleaned_data.get("line1"),
                line2=form.cleaned_data.get("line2"),
                city=form.cleaned_data.get("city"),
                province=form.cleaned_data.get("province"),
                postal_code=form.cleaned_data.get("postal_code"),
            )

            social_links = SocialMediaLink.objects.create(
                user=user,
                instagram=form.cleaned_data.get("instagram"),
                facebook=form.cleaned_data.get("facebook"),
                twitter=form.cleaned_data.get("twitter"),
            )

            open_hours.save()
            shop_address.save()
            social_links.save()

            messages.success(request, 'Profile successfully updated')

            api_key = "xnd_development_L8LFCGlEVFmq8qcCLZKNoVnq303nlkB47u5W2TrknkwioknAn4H0KOQcFfbm7"
            xendit_instance = Xendit(api_key=api_key)
            XenPlatform = xendit_instance.XenPlatform

            xenplatform_account = XenPlatform.create_account(
                account_email=str(user.email),
                type=XenPlatformAccountType.MANAGED,
                business_profile={"business_name": str(shop_info.shop_name)}
            )
            print(xenplatform_account)

            # url = "http://127.0.0.1:8000/callback/" + str(xenplatform_account.user_id) + "/"
            # XenPlatform = xendit_instance.XenPlatform

            # ## When an Invoice is paid, our systems will send a callback to the URL
            # xenplatform_callback_url = XenPlatform.set_callback_url(
            #     type=XenPlatformURLType.INVOICE,
            #     url=url,
            # )

            return redirect('accounts:merchant-register-logo')

    context = {'form':form}
    return render(request, 'accounts/add-shop-information.html', context)

### The Set Callback URLs API allows you to set your sub-accounts' Callback URLs.
# Use your production key to set production URLs; use your development key to set development URLs.
# Note: Production callback URLs have to use the https protocol.
def accountCallback(request, user_id):
    user_id = user_id
    return HttpResponse(request.body)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopLogo(request):
    shop = ShopInformation.objects.get(user=request.user)
    form = ShopLogoForm(initial={'shop': shop})

    if request.method == 'POST':
        form = ShopLogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Logo successfully updated')
            return redirect('accounts:merchant-register-payment')

    context = {'form':form}
    return render(request, 'accounts/add-shop-logo.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopAccount(request):
    user = request.user
    form = ShopAccountForm()

    if request.method == 'POST':
        form = ShopAccountForm(request.POST)
        if form.is_valid():
            bank_info=BankAccount.objects.create(
                user=user,
                bank_name=form.cleaned_data.get("bank_name"),
                cardholder_name=form.cleaned_data.get("cardholder_name"),
                account_number=form.cleaned_data.get("account_number")
            )
            bank_info.save()

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

@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
def registerCustomerInformation(request):
    user = request.user
    form = CustomerInformationForm()

    if request.method == 'POST':
        form = CustomerInformationForm(request.POST)
        if form.is_valid():
            customer_info = CustomerInformation.objects.create(
                customer = user,
                customer_name=form.cleaned_data.get("customer_name"),
                customer_contact_number=form.cleaned_data.get("customer_contact_number"),
                customer_username=form.cleaned_data.get("customer_username"),
            )

            social_links = SocialMediaLink.objects.create(
                user=user,
                instagram=form.cleaned_data.get("instagram"),
                facebook=form.cleaned_data.get("facebook"),
            )

            customer_info.save()
            social_links.save()

            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:customer-register-address')
    
    context = {'form':form}
    return render(request, 'accounts/add-customer-information.html', context)

@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
def registerCustomerAddress(request):
    user = request.user
    form = CustomerAddressForm()

    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                user=user,
                line1=form.cleaned_data.get("line1"),
                line2=form.cleaned_data.get("line2"),
                city=form.cleaned_data.get("city"),
                province=form.cleaned_data.get("province"),
                postal_code=form.cleaned_data.get("postal_code"),
            )

            address.save()

            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:customer-register-payment')

    context = {'form':form}
    return render(request, 'accounts/add-customer-address.html', context)

@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
def registerCustomerAccount(request):
    user = request.user
    form = CustomerAccountForm()

    if request.method == 'POST':
        form = CustomerAccountForm(request.POST)
        if form.is_valid():
            bank_info = BankAccount.objects.create(
                user=user,
                bank_name=form.cleaned_data.get("bank_name"),
                cardholder_name=form.cleaned_data.get("cardholder_name"),
                account_number=form.cleaned_data.get("account_number"),
                exp_date=form.cleaned_data.get("exp_date"),
                cvv=form.cleaned_data.get("cvv"),
            )

            bank_info.save()

            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:customer-register-notifications')

    context = {'form':form}
    return render(request, 'accounts/add-customer-payment.html', context)

@login_required(login_url='accounts:customer-login')
@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
def registerCustomerNotifications(request):
    user = request.user
    form = NotificationsForm()

    if request.method == 'POST':
        form = NotificationsForm(request.POST)
        if form.is_valid():
            notifications = Notification.objects.create(
                user=user,
                sms=form.cleaned_data.get("sms"),
                email=form.cleaned_data.get("email"),
            )
            print(notifications)
            notifications.save()

            messages.success(request, 'Profile successfully updated')
            return redirect('accounts:customer-landing')

    context = {'form':form}
    return render(request, 'accounts/add-customer-notifications.html', context)

def logoutCustomer(request):
    logout(request)
    return redirect('accounts:customer-login')

@allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
def landingCustomer(request):
    context = {}
    return render(request, 'accounts/sample-customer-landing.html', context)
