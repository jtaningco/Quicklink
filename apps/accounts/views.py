from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from apps.accounts.models import *
from .forms import *
from .decorators import allowed_users, unauthenticated_merchant

# Email Verification
from django_email_verification import send_email

# XenPlatform Account Creation
from xendit import Xendit, XenPlatformAccountType, XenPlatformURLType

# ImageKit IO
import imagekit

# Create your views here.
@unauthenticated_merchant
def register_merchant(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid() and form.validate_password():
            user = User.objects.create_user(
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password1")
            )
            user.role = User.Types.MERCHANT
            user.is_active = False
            send_email(user)

            merchant_group, created = Group.objects.get_or_create(name='Merchant')
            user.groups.add(merchant_group)

            user.save()
            return redirect('accounts:merchant-email-verification', user.id)
    context = {'form':form}
    return render(request, 'accounts/merchant-register.html', context)

@csrf_exempt
@unauthenticated_merchant
def email_verification(request, user_id):
    user = User.objects.get(id=user_id)
    if request.is_ajax and request.method == "POST":
        send_email(user)

    context = {'user': user}
    return render(request, 'accounts/email-verification.html', context)

@csrf_exempt
@unauthenticated_merchant
def email_confirmation(request):
    if request.is_ajax:
        userId = request.POST.get('userId')
        user = User.objects.get(id=userId)
        if request.POST.get('message') == 'success':
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/user/merchant/shop/')
        if request.POST.get('message') == 'failure':
            send_email(user)
    return render(request, 'accounts/email-confirmation.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopInformation(request):
    user = request.user

    if hasattr(user, 'info_shop'):
        shop = user.info_shop
        form = ShopInformationForm(initial={
            'shop_name': shop.shop_name,
            'shop_contact_number': shop.shop_contact_number,
            'shop_username': shop.shop_username,
            'shop_email': shop.shop_email,
            'line1' : user.user_address.line1,
            'line2' : user.user_address.line2,
            'city' : user.user_address.city,
            'province' : user.user_address.province,
            'postal_code' : user.user_address.postal_code,
            'instagram' : user.user_links.instagram,
            'facebook' : user.user_links.facebook,
            'twitter' : user.user_links.twitter,
        })
    else:
        form = ShopInformationForm()
    
    if request.method == 'POST':
        form = ShopInformationForm(request.POST)
        if form.is_valid():
            shop_info, created = ShopInformation.objects.get_or_create(user=user)
            shop_info.shop_name = form.cleaned_data.get("shop_name")
            shop_info.shop_contact_number = form.cleaned_data.get("shop_contact_number").strip()
            shop_info.shop_username = form.cleaned_data.get("shop_username")
            shop_info.shop_email = form.cleaned_data.get("shop_email")
            shop_info.save()

            shop_address, created = Address.objects.get_or_create(user=user)
            shop_address.line1 = form.cleaned_data.get("line1")
            shop_address.line2 = form.cleaned_data.get("line2")
            shop_address.city = form.cleaned_data.get("city")
            shop_address.province = form.cleaned_data.get("province")
            shop_address.postal_code = form.cleaned_data.get("postal_code")
            shop_address.save()

            social_links, created = SocialMediaLink.objects.get_or_create(user=user)
            social_links.instagram = form.cleaned_data.get("instagram")
            social_links.facebook = form.cleaned_data.get("facebook")
            social_links.twitter = form.cleaned_data.get("twitter")
            social_links.save()

            # api_key = "xnd_development_L8LFCGlEVFmq8qcCLZKNoVnq303nlkB47u5W2TrknkwioknAn4H0KOQcFfbm7"
            # xendit_instance = Xendit(api_key=api_key)
            # XenPlatform = xendit_instance.XenPlatform

            # xenplatform_account = XenPlatform.create_account(
            #     account_email=str(user.email),
            #     type=XenPlatformAccountType.MANAGED,
            #     business_profile={"business_name": str(shop_info.shop_name)}
            # )
            # print(xenplatform_account)

            # url = "http://127.0.0.1:8000/callback/" + str(xenplatform_account.user_id) + "/"
            # XenPlatform = xendit_instance.XenPlatform

            # ## When an Invoice is paid, our systems will send a callback to the URL
            # xenplatform_callback_url = XenPlatform.set_callback_url(
            #     type=XenPlatformURLType.INVOICE,
            #     url=url,
            # )

            return redirect('accounts:merchant-add-logo')

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
    
    if hasattr(shop, 'logo_shop'):
        form = ShopLogoForm(initial={'logo':shop.logo_shop.logo})
        print(shop.logo_shop.logo)
    else:
        form = ShopLogoForm()

    if request.method == 'POST':
        form = ShopLogoForm(request.POST, request.FILES)
        if form.is_valid():
            shop_logo, created = ShopLogo.objects.get_or_create(shop=shop)
            shop_logo.logo = form.cleaned_data.get('logo')
            shop_logo.save()
            return redirect('accounts:merchant-add-settings')

    context = {'form':form, 'shop':shop}
    return render(request, 'accounts/add-shop-logo.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopSettings(request):
    shop = ShopInformation.objects.get(user=request.user)
    selected_dates = []
    selected_radio = ""
    
    if hasattr(shop, 'shop_general_settings'):
        if shop.shop_general_settings.cutoff_time != None:
            form = ShopSettingsForm(initial={
                'shop_cod':shop.shop_general_settings.shop_cod,
                'delivery_days':shop.shop_general_settings.delivery_days,
                'cutoff_time':shop.shop_general_settings.cutoff_time,
                'from_hour':shop.shop_general_settings.delivery_from_hour,
                'to_hour':shop.shop_general_settings.delivery_to_hour,
            })
            selected_radio = "cutoff_time"
        elif shop.shop_general_settings.cutoff_days != None:
            form = ShopSettingsForm(initial={
                'shop_cod':shop.shop_general_settings.shop_cod,
                'delivery_days':shop.shop_general_settings.delivery_days,
                'cutoff_days':shop.shop_general_settings.cutoff_days,
                'from_hour':shop.shop_general_settings.delivery_from_hour,
                'to_hour':shop.shop_general_settings.delivery_to_hour,
            })
            selected_radio = "cutoff_days"
        else:
            form = ShopSettingsForm(initial={
                'shop_cod':shop.shop_general_settings.shop_cod,
                'delivery_days':shop.shop_general_settings.delivery_days,
                'from_hour':shop.shop_general_settings.delivery_from_hour,
                'to_hour':shop.shop_general_settings.delivery_to_hour,
            })

        selected_dates = WEEKDAYS.get_selected_values(shop.shop_general_settings.delivery_days)
    else:
        form = ShopSettingsForm()

    if request.method == 'POST':
        form = ShopSettingsForm(request.POST)
        if form.is_valid():
            shop_settings, created = ShopGeneralSettings.objects.get_or_create(shop=shop)
            shop_settings.delivery_days=form.cleaned_data.get('delivery_days')
            shop_settings.delivery_from_hour=form.cleaned_data.get('from_hour')
            shop_settings.delivery_to_hour=form.cleaned_data.get('to_hour')

            radio_cutoff_time = request.POST.get("radio-cutoff-time", None)
            radio_cutoff_days = request.POST.get("radio-cutoff-days", None)

            if radio_cutoff_time is not None:
                shop_settings.cutoff_time=form.cleaned_data.get('cutoff_time')
                shop_settings.cutoff_days=None
            elif radio_cutoff_days is not None:
                shop_settings.cutoff_days=form.cleaned_data.get('cutoff_days')
                shop_settings.cutoff_time=None

            if 'shop_cod' in request.POST:
                shop_settings.shop_cod=form.cleaned_data.get('shop_cod')

            shop_settings.save()
        return redirect('accounts:merchant-add-delivery')
    context = {'form':form, 'selected_dates':selected_dates, 'selected_radio':selected_radio}
    return render(request, 'accounts/add-shop-settings.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopDeliveries(request):
    shop = ShopInformation.objects.get(user=request.user)
    use_same_address = False
    
    if hasattr(shop, 'shop_delivery_settings'):
        form = DeliverySettingsForm(initial={
            'seller_books': shop.shop_delivery_settings.seller_books,
            'shop_delivery_fees': shop.shop_delivery_fees,
            'buyer_books': shop.shop_delivery_settings.buyer_books,
            'buyer_picks_up': shop.shop_delivery_settings.buyer_picks_up,
            'line1': shop.shop_delivery_settings.line1,
            'line2': shop.shop_delivery_settings.line2,
            'city': shop.shop_delivery_settings.city,
            'province': shop.shop_delivery_settings.province,
            'postal_code': shop.shop_delivery_settings.postal_code
        })
        if shop.shop_delivery_settings.line1 == shop.user.user_address.line1:
            use_same_address = True
    else:
        form = DeliverySettingsForm()

    if request.method == 'POST':
        form = DeliverySettingsForm(request.POST)
        if form.is_valid():
            shop_delivery_settings, created = ShopDeliverySettings.objects.get_or_create(shop=shop)
            if 'seller_books' in request.POST:
                shop_delivery_settings.seller_books = True
                shop.shop_delivery_fees = form.clean_delivery_fees()
                shop.save()
            else:
                shop_delivery_settings.seller_books = False
                shop.shop_delivery_fees = None
                shop.save()
            
            if 'buyer_books' in request.POST:
                shop_delivery_settings.buyer_books = True
            else:
                shop_delivery_settings.buyer_books = False

            if 'buyer_picks_up' in request.POST:
                shop_delivery_settings.buyer_picks_up = True
            else:
                shop_delivery_settings.buyer_picks_up = False

            if form.cleaned_data.get('buyer_books') == True or form.cleaned_data.get('buyer_picks_up') == True:
                if 'use_shop_address' in request.POST:
                    shop_delivery_settings.line1 = shop.user.user_address.line1
                    shop_delivery_settings.line2 = shop.user.user_address.line2
                    shop_delivery_settings.city = shop.user.user_address.city
                    shop_delivery_settings.province = shop.user.user_address.province
                    shop_delivery_settings.postal_code = shop.user.user_address.postal_code
                else:    
                    shop_delivery_settings.line1 = form.cleaned_data.get('line1')
                    shop_delivery_settings.line2 = form.cleaned_data.get('line2')
                    shop_delivery_settings.city = form.cleaned_data.get('city')
                    shop_delivery_settings.province = form.cleaned_data.get('province')
                    shop_delivery_settings.postal_code = form.cleaned_data.get('postal_code')
            shop_delivery_settings.save()
        return redirect('accounts:merchant-add-payment')

    context = {'form':form, 'use_same_address':use_same_address}
    return render(request, 'accounts/add-shop-deliveries.html', context)

@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def registerShopAccount(request):
    user = request.user

    if hasattr(user, 'user_account'):
        form = ShopAccountForm(initial={
            'bank_name': user.user_account.bank_name,
            'cardholder_name': user.user_account.cardholder_name,
            'account_number': user.user_account.account_number,
        })
    else:
        form = ShopAccountForm()

    if request.method == 'POST':
        form = ShopAccountForm(request.POST)
        if form.is_valid():
            bank_info, created = BankAccount.objects.get_or_create(user=user)
            bank_info.bank_name = form.cleaned_data.get('bank_name')
            bank_info.cardholder_name = form.cleaned_data.get('cardholder_name')
            bank_info.account_number = form.cleaned_data.get('account_number')
            bank_info.save()
            
            messages.success(request, 'Profile successfully registered!')
            return redirect('products:products')

    context = {'form':form}
    return render(request, 'accounts/add-shop-account.html', context)

@unauthenticated_merchant
def loginMerchant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if not hasattr(user, 'info_shop'):
                return redirect('accounts:merchant-add-shop')
            else:
                return redirect('products:products')
        else:
            messages.info(request, "Email or password is incorrect.")
            return redirect ('accounts:merchant-login')
    
    context = {}
    return render(request, 'accounts/merchant-login.html', context)

def logout_user(request):
    logout(request)
    return redirect('accounts:merchant-login')

# @unauthenticated_customer
# def registerCustomer(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = User.objects.create(
#                 username=form.cleaned_data.get("username"),
#                 email=form.cleaned_data.get("email"),
#                 role=form.cleaned_data.get("role"),
#             )
#             user.set_password(form.cleaned_data.get("password"))
#             user.save()

#             username = form.cleaned_data.get('username')
#             messages.success(request, 'Account successfully created for ' + username)
#             return redirect('accounts:customer-login')

#     context = {'form':form}
#     return render(request, 'accounts/customer-register.html', context)

# @unauthenticated_customer
# def loginCustomer(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('accounts:customer-landing')
#         else:
#             messages.info(request, "Username or password is incorrect.")
    
#     context = {}
#     return render(request, 'accounts/customer-login.html', context)

# @login_required(login_url='accounts:customer-login')
# @allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
# def registerCustomerInformation(request):
#     user = request.user
#     form = CustomerInformationForm()

#     if request.method == 'POST':
#         form = CustomerInformationForm(request.POST)
#         if form.is_valid():
#             customer_info = CustomerInformation.objects.create(
#                 customer = user,
#                 customer_name=form.cleaned_data.get("customer_name"),
#                 customer_contact_number=form.cleaned_data.get("customer_contact_number"),
#                 customer_username=form.cleaned_data.get("customer_username"),
#             )

#             social_links = SocialMediaLink.objects.create(
#                 user=user,
#                 instagram=form.cleaned_data.get("instagram"),
#                 facebook=form.cleaned_data.get("facebook"),
#             )

#             customer_info.save()
#             social_links.save()

#             messages.success(request, 'Profile successfully updated')
#             return redirect('accounts:customer-register-address')
    
#     context = {'form':form}
#     return render(request, 'accounts/add-customer-information.html', context)

# @login_required(login_url='accounts:customer-login')
# @allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
# def registerCustomerAddress(request):
#     user = request.user
#     form = CustomerAddressForm()

#     if request.method == 'POST':
#         form = CustomerAddressForm(request.POST)
#         if form.is_valid():
#             address = Address.objects.create(
#                 user=user,
#                 line1=form.cleaned_data.get("line1"),
#                 line2=form.cleaned_data.get("line2"),
#                 city=form.cleaned_data.get("city"),
#                 province=form.cleaned_data.get("province"),
#                 postal_code=form.cleaned_data.get("postal_code"),
#             )

#             address.save()

#             messages.success(request, 'Profile successfully updated')
#             return redirect('accounts:customer-register-payment')

#     context = {'form':form}
#     return render(request, 'accounts/add-customer-address.html', context)

# @login_required(login_url='accounts:customer-login')
# @allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
# def registerCustomerAccount(request):
#     user = request.user
#     form = CustomerAccountForm()

#     if request.method == 'POST':
#         form = CustomerAccountForm(request.POST)
#         if form.is_valid():
#             bank_info = BankAccount.objects.create(
#                 user=user,
#                 bank_name=form.cleaned_data.get("bank_name"),
#                 cardholder_name=form.cleaned_data.get("cardholder_name"),
#                 account_number=form.cleaned_data.get("account_number"),
#                 exp_date=form.cleaned_data.get("exp_date"),
#                 cvv=form.cleaned_data.get("cvv"),
#             )

#             bank_info.save()

#             messages.success(request, 'Profile successfully updated')
#             return redirect('accounts:customer-register-notifications')

#     context = {'form':form}
#     return render(request, 'accounts/add-customer-payment.html', context)

# @login_required(login_url='accounts:customer-login')
# @allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
# def registerCustomerNotifications(request):
#     user = request.user
#     form = NotificationsForm()

#     if request.method == 'POST':
#         form = NotificationsForm(request.POST)
#         if form.is_valid():
#             notifications = Notification.objects.create(
#                 user=user,
#                 sms=form.cleaned_data.get("sms"),
#                 email=form.cleaned_data.get("email"),
#             )
#             print(notifications)
#             notifications.save()

#             messages.success(request, 'Profile successfully updated')
#             return redirect('accounts:customer-landing')

#     context = {'form':form}
#     return render(request, 'accounts/add-customer-notifications.html', context)

# @allowed_users(allowed_roles=[User.Types.CUSTOMER, User.Types.ADMIN])
# def landingCustomer(request):
#     context = {}
#     return render(request, 'accounts/sample-customer-landing.html', context)