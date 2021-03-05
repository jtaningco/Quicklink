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
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)