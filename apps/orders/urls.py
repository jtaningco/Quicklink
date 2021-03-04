from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='order-summary'),
    path('delete-order/<str:order_pk>/', views.deleteOrder, name='delete-order'),
    path('preview/', views.menuPreview, name='menu-preview'),
    path('preview/<str:pk>/order', views.addPreviewOrder, name='preview-order'),
    path('pending/', views.pendingOrders, name='pending-orders' ),
    path('shops/', views.viewShops, name='view-shops'),
    path('shops/<str:shop_pk>/products', views.viewProducts, name='view-products'),
    path('shops/<str:shop_pk>/products/<str:product_pk>/', views.addOrder, name='add-order'),
    path('shops/<str:shop_pk>/products/<str:product_pk>/add/', views.updateItem, name='update-item'),
    path('shops/<str:shop_pk>/checkout/', views.checkout, name='checkout'),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)