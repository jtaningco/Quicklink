from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('merchant/register/', views.register_merchant, name='merchant-register'),
    path('merchant/<str:user_id>/confirmation/', views.email_confirmation, name='merchant-email-confirmation'),
    path('merchant/register/shop', views.registerShopInformation, name='merchant-register-shop'),
    path('merchant/register/logo', views.registerShopLogo, name='merchant-register-logo'),
    path('merchant/register/payment', views.registerShopAccount, name='merchant-register-payment'),
    path('merchant/login/', views.loginMerchant, name='merchant-login'),
    path('merchant/logout/', views.logoutMerchant, name='merchant-logout'),
    path('customer/register/', views.registerCustomer, name='customer-register'),
    path('customer/register/info', views.registerCustomerInformation, name='customer-register-info'),
    path('customer/register/address', views.registerCustomerAddress, name='customer-register-address'),
    path('customer/register/payment', views.registerCustomerAccount, name='customer-register-payment'),
    path('customer/register/notifications', views.registerCustomerNotifications, name='customer-register-notifications'),
    path('customer/login/', views.loginCustomer, name='customer-login'),
    path('customer/logout/', views.logoutCustomer, name='customer-logout'),
    path('customer/landing/', views.landingCustomer, name='customer-landing'),
    path('callback/<str:user_id>/', views.accountCallback, name='xendit-callback'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)