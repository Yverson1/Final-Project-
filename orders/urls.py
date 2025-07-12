# orders/urls.py

from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    OrderListView,  OrderCreateView
)

urlpatterns = [
    path('products/',         ProductListView.as_view(),    name='product-list'),
    path('products/<int:pk>/',ProductDetailView.as_view(),  name='product-detail'),
    path('orders/',           OrderListView.as_view(),      name='order-list'),
    path('orders/create/',    OrderCreateView.as_view(),    name='order-create'),
]

