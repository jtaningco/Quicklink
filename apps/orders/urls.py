from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='order-summary'),
    path('delete-order/<str:order_pk>/', views.deleteOrder, name='delete-order'),
    path('products-list/', views.viewProducts, name='products-list'),
    path('products-list/<str:pk>/order', views.addOrder, name='add-order'),
    path('pending/', views.pendingOrders, name='pending-orders' ),
    path('pending/today', views.pendingToday, name='pending-today'),
    path('pending/next-seven-days', views.pendingNextSevenDays, name='pending-next-seven-days')
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)