from django.contrib import admin
from .models import User, ShopInformation, CustomerInformation
from django.contrib.auth import get_user_model

# Register your models here.
admin.site.register(User)
admin.site.register(ShopInformation)
admin.site.register(CustomerInformation)