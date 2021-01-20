from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == "MERCHANT":
                return redirect('products:products')
            else:
                return redirect('accounts:customer-landing')
        else:        
            return view_func(request, *args, **kwargs)

    return wrapper_func

def merchants_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        role = request.user.role
        if role == 'CUSTOMER':
            return redirect('accounts:customer-landing')

        if role == 'MERCHANT':
            return view_func(request, *args, **kwargs)

        return wrapper_func