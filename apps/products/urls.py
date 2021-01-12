from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('product/<str:product_pk>/', views.productDetails, name='product'),
    path('add/', views.addProduct, name='add-product'),
    path('product/<str:product_pk>/update', views.updateProduct, name='update-product'),
    path('product/<str:product_pk>/delete', views.deleteProduct, name='delete-product')
]