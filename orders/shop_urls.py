from django.urls import path
from .views import (
    product_detail, cart_html, add_to_cart,
    order_create_html, thank_you, ProductListHTMLView
)

urlpatterns = [
    path('product/<int:pk>/', product_detail, name='product-detail-html'),
    path('cart/', cart_html, name='cart'),
    path('cart/add/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('order/create/', order_create_html, name='order-create-html'),
    path('order/thank-you/', thank_you, name='thank-you'),
    path('', ProductListHTMLView.as_view(), name='products'),
]



