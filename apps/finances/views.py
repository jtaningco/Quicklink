from django.shortcuts import render

# Create your views here.
@login_required(login_url='accounts:merchant-login')
@allowed_users(allowed_roles=[User.Types.MERCHANT, User.Types.ADMIN])
def totalRevenue(request):
    user = request.user
    orders = Order.objects.filter(shop=user)