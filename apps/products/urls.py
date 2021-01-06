from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<str:pk>/', views.productDetails, name='product'),
    path('add-product/', views.addProduct, name='add-product'),
    path('update-product/<str:pk>/', views.updateProduct, name='update-product'),
]