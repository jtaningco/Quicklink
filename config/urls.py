"""QuicklinkDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from config import settings

from django_email_verification import urls as email_urls

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('verification/', include(email_urls)),
    path('', include(('customers.urls', 'customers'), namespace='customers')),
    path('user/', include(('accounts.urls', 'accounts'), namespace='users')),
    path('shop/orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('shop/products/', include(('products.urls', 'products'), namespace='products')),
]

urlpatterns += static (settings.dev.MEDIA_URL, document_root=settings.dev.MEDIA_ROOT)