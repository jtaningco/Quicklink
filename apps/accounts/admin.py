from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User)
admin.site.register(ShopInformation)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(SocialMediaLink)
admin.site.register(DeliveryDays)