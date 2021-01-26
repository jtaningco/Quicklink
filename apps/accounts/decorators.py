from django.http import HttpResponse
from django.shortcuts import redirect

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

def allowed_users(allowed_role):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = None

            if not request.user.role:
                role = None
            else:
                role = request.user.role
            
            if role == allowed_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator
