from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('add/', views.addProduct, name='add-product'),
    path('set-active/', views.setProductsAsActive, name='set-product-active'),
    path('set-inactive/', views.setProductsAsInactive, name='set-products-inactive'),
    path('delete-selected/', views.deleteSelectedProducts, name='delete-selected-products'),
    path('product/<str:product_pk>/', views.productDetails, name='product'),
    path('product/<str:product_pk>/update/', views.updateProduct, name='update-product'),
    path('product/<str:product_pk>/duplicate/', views.duplicateProduct, name='duplicate-product'),
    path('product/<str:product_pk>/delete/', views.deleteProduct, name='delete-product')
]