from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.viewShops, name='view-shops'),
    path('shops/<str:shop_pk>/products/', views.viewProducts, name='view-products'),
    path('shops/<str:shop_pk>/products/<str:product_pk>/', views.addOrder, name='add-order'),
    path('shops/<str:shop_pk>/products/<str:product_pk>/add/', views.addItem, name='add-item'),
    path('shops/<str:shop_pk>/products/<str:product_pk>/edit/', views.updateItem, name='update-item'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/payment/', views.payment, name='payment'),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)