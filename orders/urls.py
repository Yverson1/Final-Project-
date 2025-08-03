from django.urls import path
from orders.views import cart_html
urlpatterns = [
    path('cart/', cart_html, name='cart'),
    ...
]

from .views import (
    ProductListView, ProductDetailView,
    OrderListView, OrderCreateView,
    ProductListHTMLView, product_detail,
    add_to_cart, cart_html, order_create_html,
    thank_you, redirect_to_products
)

urlpatterns = [
    # HTML views
    path('', redirect_to_products, name='home'),
    path('products/', ProductListHTMLView.as_view(), name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('cart/', cart_html, name='cart'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('order/', order_create_html, name='order-form'),
    path('thank-you/', thank_you, name='thank-you'),

    # API views
    path('api/products/', ProductListView.as_view(), name='api-product-list'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='api-product-detail'),
    path('api/orders/', OrderListView.as_view(), name='api-order-list'),
    path('api/orders/create/', OrderCreateView.as_view(), name='api-order-create'),
]
