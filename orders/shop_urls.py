# orders/shop_urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',             views.product_list_html,    name='product-list-html'),
    path('product/<int:pk>/', views.product_detail_html, name='product-detail-html'),
    path('cart/',        views.cart_html,            name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart,    name='add-to-cart'),
    path('order/create/', views.order_create_html,   name='order-create-html'),
    path('order/thank-you/', views.thank_you,        name='thank-you'),
]


