from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('add-product/', views.addProduct, name='add-product'),
]