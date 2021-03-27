from django.http import HttpResponse
from django.shortcuts import redirect
from apps.accounts.models import ShopInformation

def unauthenticated_merchant(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:products')
        else:        
            return view_func(request, *args, **kwargs)

    return wrapper_func

def unauthenticated_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:customer-landing')
        else:        
            return view_func(request, *args, **kwargs)

    return wrapper_func

def setup_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not hasattr(request.user, 'shop_info'):
            return redirect('accounts:merchant-add-shop')
        elif not hasattr(request.user.shop_info, 'shop_logo'):
            return redirect('accounts:merchant-add-logo')
        elif not hasattr(request.user.shop_info, 'shop_general_settings'):
            return redirect('accounts:merchant-add-settings')
        elif not hasattr(request.user.shop_info, 'shop_delivery_settings'):
            return redirect('accounts:merchant-add-delivery')
        elif not hasattr(request.user, 'user_account'):
            return redirect('accounts:merchant-add-payment')
        else:        
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = None

            if not request.user.role:
                role = None
            else:
                role = request.user.role
            
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator
