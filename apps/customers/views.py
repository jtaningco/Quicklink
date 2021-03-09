from django.shortcuts import render, redirect
from django.utils.timezone import datetime, timedelta

from apps.products.models import Product, Size, Addon
from apps.orders.models import Order, ProductOrder, OrderInformation
from apps.accounts.models import *

from apps.orders.forms import OrderForm, CheckoutForm, CardForm

from django.http import HttpResponse, JsonResponse
from decimal import Decimal
import json
import shortuuid
from secret_key_generator import secret_key_generator

from xendit import Xendit, Balance
import jwt
import base64

# Create your views here.
# View Products (Customers)
def viewShops(request):
    users = User.objects.filter(role=User.Types.MERCHANT)
    allShops = ShopInformation.objects.all()
    shops = []

    for shop in allShops:
        if shop.user in users:
            shops.append(shop)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'shops':shops, 'items':items, 'order':order}
    return render(request, 'customers/shops.html', context)

# View Products (Customers)
def viewProducts(request, shop_pk):
    shop = ShopInformation.objects.get(id=shop_pk)
    user = shop.user
    products = Product.objects.filter(user=shop.user)
    sizes = Size.objects.filter(product__in=products)

    size_prices = []

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

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

    context = {'products':products, 'shop':shop, 'user':user, 'sizes':sizes, 'items':items, 'order':order, 'shop':shop}
    return render(request, 'customers/products.html', context)

# Add Products to Cart (Customers)
def addOrder(request, shop_pk, product_pk):
    user = request.user
    shop = ShopInformation.objects.get(id=shop_pk)
    shopOwner = shop.user

    product = Product.objects.get(id=product_pk)

    sizes = Size.objects.filter(product=product)
    addons = Addon.objects.filter(product=product)
    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()
        form = OrderForm(initial={
            'product': product, 'order': order
        })
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        form = OrderForm(initial={
            'product': product
        })

    if request.method == 'POST':
        # Check if order form exists        
        form = OrderForm(request.POST, product=product)

        # Save form if form is valid
        if form.is_valid():
            product.sold = product.sold + 1
            if product.stock == 'Made to Order':
                pass
            else:
                product.stock = str(int(product.stock) - 1)
                product.save()
            return redirect('add/')
        else:
            form = OrderForm(data=request.POST)
            print(form.errors.as_data())
            return HttpResponse('Order failed!')

    context = {'form':form, 'product':product, 'sizes':sizes, 'addons':addons, 'shop':shop, 'order':order}
    return render(request, 'customers/order_form.html', context)

def addItem(request, shop_pk, product_pk):
    data = json.loads(request.body)
    form = data['form']
    shopId = data['shopId']
    productId = data['productId']
    action = data['action']

    addons_list = []
    quantity = 1

    for i in form:
        if i.get('name') == 'size':
            size = Size.objects.get(id=i.get('value'))
        
        if i.get('name') == 'addons':
            addons_list.append(i.get('value'))
        
        if i.get('name') == 'instructions':
            instructions = i.get('value')
        
        if i.get('name') == 'quantity':
            quantity = int(i.get('value'))
    
    addons = Addon.objects.filter(id__in=addons_list)

    customer = request.user
    shop = ShopInformation.objects.get(id=shopId)
    shopOwner = shop.user

    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)

    if addons:
        addons_total = 0
        for i in addons:
            addons_total += (quantity * i.price_addon)
        total = (quantity * size.price_size) + addons_total
    else:    
        total = (quantity * size.price_size)

    productOrder, created = ProductOrder.objects.get_or_create(
        order=order, product=product, size=size, addons__in=addons,
        instructions=instructions, quantity=quantity, total=total)

    for addon in addons:
        productOrder.addons.add(addon)

    productOrder.save()
    
    order.subtotal = 0
    for product in order.productorder_set.all():
        order.subtotal += product.total

    order.fees = order.subtotal * Decimal(0.05)
    order.total = order.subtotal + order.fees
    order.save()

    return redirect('/shops/')

def updateItem(request, shop_pk, product_pk):
    data = json.loads(request.body)
    shopId = data['shopId']
    itemId = data['itemId']
    productId = data['productId']
    action = data['action']

    productOrder = ProductOrder.objects.get(id=itemId)
    order = productOrder.order
    addons = productOrder.addons.all()

    if action == "increase":
        productOrder.quantity = (productOrder.quantity + 1)
    elif action == "decrease":
        productOrder.quantity = (productOrder.quantity - 1)

    if addons:
        addons_total = 0
        for i in addons:
            addons_total += (productOrder.quantity * i.price_addon)
        productOrder.total = (productOrder.quantity * productOrder.size.price_size) + addons_total
    else:    
        productOrder.total = (productOrder.quantity * productOrder.size.price_size)

    productOrder.save()

    if productOrder.quantity <= 0:
        productOrder.delete()
    
    order.subtotal = 0
    for product in order.productorder_set.all():
        order.subtotal += product.total

    order.fees = order.subtotal * Decimal(0.05)
    order.total = order.subtotal + order.fees
    order.save()

    return JsonResponse('Item was edited', safe=False)

def checkout(request):    
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.productorder_set.all()

        highest_days = 0
        for item in items:
            if item.product.days > highest_days: 
                highest_days = item.product.days
        min_date = datetime.today() + timedelta(days=highest_days+1)
    else:
        customer = None
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []

        highest_days = 0
        for item in items:
            if item.product.days > highest_days: 
                highest_days = item.product.days
        min_date = datetime.today() + timedelta(days=highest_days+1)
        
    form = CheckoutForm(min_date=min_date, user=customer)

    if request.method == "POST":
        form = CheckoutForm(data=request.POST or None, min_date=min_date, user=customer)
        if form.is_valid():
            sessionSender = CustomerInformation.objects.create(
                customer_name = form.cleaned_data.get('name'),
                customer_email = form.cleaned_data.get('email'),
                customer_contact_number = form.cleaned_data.get('contact_number')
            )
            sessionSender.save()
                
            sessionAddress = Address.objects.create(
                line1 = form.cleaned_data.get('line1'),
                line2 = form.cleaned_data.get('line2'),                
                city = form.cleaned_data.get('city'),
                province = form.cleaned_data.get('province'),
                postal_code = form.cleaned_data.get('postal_code'),
            )
            sessionAddress.save()

            orderNotifications = Notification.objects.create(
                sms = form.cleaned_data.get('notif_sms'),
                email = form.cleaned_data.get('notif_email')
            )
            orderNotifications.save()

            orderInfo = OrderInformation.objects.create(
                order = order,
                session_sender = sessionSender,
                session_address = sessionAddress,
                session_notifications = orderNotifications,
            )
            orderInfo.save()
            
            bankAccount = form.cleaned_data.get('bank_name')

            # If Debit/Credit
            if bankAccount in CheckoutForm.BANKS[0]:
                return redirect('payment/card/')
            
            # If eWallet
            elif bankAccount in CheckoutForm.BANKS[1]:
                return redirect('payment/ewallet/')

            # if COD
            else:
                return redirect('payment/cod/')
        else:
            print(form.errors.as_data())

    context = {'items':items, 'order':order, 'form':form}
    return render(request, 'customers/checkout.html', context)

def payment(request, slug):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(user=customer, complete=False)
        items = order.productorder_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    # If Debit/Credit
    if slug == 'card':
        try:
            form = CardForm(initial={
                'currency':"PHP",
                'amount': order.total,
                'cardholder_name': customer.user_account.cardholder_name,
                'account_number': customer.user_account.account_number,
                'exp_date': customer.user_account.exp_date,
            })
        except:
            form = CardForm(initial={
                'currency':"PHP",
                'amount': order.total,
            })
            
    # If eWallet
    elif slug == 'ewallet':
        form = CardForm(initial={
                'currency':"PHP",
                'amount': order.total,
            })
    # if COD
    else:
        form = CardForm(initial={
                'currency':"PHP",
                'amount': order.total,
            })

    orderInfo = OrderInformation.objects.get(order=order)
    customer_name = orderInfo.session_sender.customer_name.split(' ')
    given_names_list = []
    for name in customer_name:
        if name != customer_name[-1]:
            given_names_list.append(str(name))
        else:
            surname = str(name)
        given_names = ' '.join(given_names_list)

    contact_number = orderInfo.session_sender.customer_contact_number
    mobile_number_list = []
    
    for number in contact_number:
        mobile_number_list.append(number)
    mobile_number_list[0] = '(+63)('
    mobile_number_list[-1] = mobile_number_list[-1] + ')'
    mobile_number = ''.join(mobile_number_list)

    if request.method == 'POST' and slug == 'card':
        form = CardForm(request.POST)
        if form.is_valid():
            exp_month = str(form.cleaned_data.get('exp_date').split('/')[0])
            if len(form.cleaned_data.get('exp_date').split('/')[1]) == 2:
                exp_year = str('20' + form.cleaned_data.get('exp_date').split('/')[1])
            elif len(form.cleaned_data.get('exp_date').split('/')[1]) == 4:
                exp_year = str(form.cleaned_data.get('exp_date').split('/')[1])
            card_number_list = form.cleaned_data.get("account_number").split(' ')
            card_number = ''.join(card_number_list)
            card_cvn = form.cleaned_data.get("cvv")
            data = {
                "amount": str(order.total),
                "card_number": card_number,
                "card_exp_month": exp_month,
                "card_exp_year": exp_year,
                "card_cvn": str(card_cvn),
                "is_multiple_use": False,
                "should_authenticate": True,
                "currency": "PHP",
                "on_behalf_of": "",
                "billing_details": {
                    "given_names": given_names,
                    "surname": surname,
                    "email": orderInfo.session_sender.customer_email,
                    "mobile_number": orderInfo.session_sender.customer_contact_number,
                    "phone_number": orderInfo.session_sender.customer_contact_number,
                    "address": {
                        "country": "PH",
                        "street_line1": orderInfo.session_address.line1,
                        "street_line2": orderInfo.session_address.line2,
                        "city": orderInfo.session_address.city,
                        "province_state": orderInfo.session_address.province,
                        "postal_code": orderInfo.session_address.postal_code
                    } 
                }
            }

            private_key = secret_key_generator.generate(len_of_secret_key=15)
            public_key = secret_key_generator.generate(len_of_secret_key=15)

            orderInfo.token_private_key = private_key
            orderInfo.token_public_key = public_key

            orderInfo.token_jwt_id = jwt.encode(
                data, 
                private_key, 
                algorithm="HS256"
            )
            orderInfo.save()
            return redirect('token/', slug)
        else:
            data = form.errors.as_json()
            return JsonResponse(data, status=400)

    if request.method == 'POST' and slug == 'ewallet':
        form = CardForm(request.POST)
        if form.is_valid():
            # Create Customer Object
            # Include Metadata to store more data for analysis
            random_uuid = str(shortuuid.uuid())
            reference_id = "quicklink_customer-" + random_uuid

            api_key = "xnd_development_P4qDfOss0OCpl8RtKrROHjaQYNCk9dN5lSfk+R1l9Wbe+rSiCwZ3jw=="
            xendit_instance = Xendit(api_key=api_key)
            DirectDebit = xendit_instance.DirectDebit

            data = {
                "reference_id": reference_id,
                "email": orderInfo.session_sender.customer_email,
                "mobile_number": mobile_number,
                "description": "eWallet Customer",
                "given_names": given_names,
                "surname": surname,
                "nationality": "PH",
                "address": {
                    "country": "PH",
                    "street_line1": orderInfo.session_address.line1,
                    "street_line2": orderInfo.session_address.line2,
                    "city": orderInfo.session_address.city,
                    "province_state": orderInfo.session_address.province,
                    "postal_code": orderInfo.session_address.postal_code 
                }
            }

            private_key = secret_key_generator.generate(len_of_secret_key=15)
            public_key = secret_key_generator.generate(len_of_secret_key=15)

            orderInfo.token_private_key = private_key
            orderInfo.token_public_key = public_key

            orderInfo.token_jwt_id = jwt.encode(
                data, 
                private_key, 
                algorithm="HS256"
            )
            orderInfo.save()
            return redirect('/checkout/payment/ewallet/callback')
        else:
            data = form.errors.as_json()
            return JsonResponse(data, status=400) 

    context = {'items':items, 'form':form, 'slug':slug, 'order':order}
    return render(request, 'customers/payment.html', context)

def eWalletCallback(request, slug):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(user=customer, complete=False)
        orderInfo = OrderInformation.objects.get(order=order)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    json_data = jwt.decode(
        orderInfo.token_jwt_id, 
        orderInfo.token_public_key, 
        algorithms=["HS256"]
    )

    return JsonResponse(json_data, status=200) 


def createToken(request, slug):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(user=customer, complete=False)
        orderInfo = OrderInformation.objects.get(order=order)
    
    json_data = jwt.decode(
        orderInfo.token_jwt_id, 
        orderInfo.token_public_key, 
        algorithms=["HS256"]
    )
    data = json.dumps(json_data)
    
    if request.is_ajax and request.method == 'POST':
        if request.POST.get('token_id') != None:
            token_id = request.POST.get('token_id')
        if request.POST.get('auth_id') != None:
            auth_id = request.POST.get('auth_id')

    if "token_id" in locals():
        json_data['token_id'] = token_id
        orderInfo.token_jwt_id = jwt.encode(json_data, orderInfo.token_private_key, algorithm="HS256")
        orderInfo.save()
        
    if "auth_id" in locals():
        json_data['authentication_id'] = auth_id
        orderInfo.token_jwt_id = jwt.encode(json_data, orderInfo.token_private_key, algorithm="HS256")
        orderInfo.save()
        return redirect('/checkout/payment/card/auth/')

    context = {'data':data}
    return render(request, 'customers/token.html', context)

def createAuthorization(request, slug):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(user=customer, complete=False)
        orderInfo = OrderInformation.objects.get(order=order)
    
    data = jwt.decode(
        orderInfo.token_jwt_id, 
        orderInfo.token_public_key, 
        algorithms=["HS256"]
    )
    print(data)

    api_key = "xnd_development_L8LFCGlEVFmq8qcCLZKNoVnq303nlkB47u5W2TrknkwioknAn4H0KOQcFfbm7"
    xendit_instance = Xendit(api_key=api_key)
    CreditCard = xendit_instance.CreditCard

    token_id = str(data['token_id'])
    auth_id = str(data['authentication_id'])
    amount = float(data['amount'])
    card_cvn = str(data['card_cvn'])
    random_uuid = str(shortuuid.uuid())
    external_id = "quicklink_charge-" + random_uuid

    charge = CreditCard.create_authorization(
        token_id=token_id,
        authentication_id=auth_id,
        external_id=external_id,
        amount=amount,
        card_cvn=card_cvn,
        currency="PHP",
    )
    print(charge)

    return HttpResponse(charge)