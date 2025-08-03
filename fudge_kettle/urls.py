from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from orders.views import cart_html, ProductListHTMLView  # ✅ Correct imports

urlpatterns = [
    path('',       TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('shop/',  include('orders.shop_urls')),  # shop HTML
    path('api/',   include('orders.urls')),       # DRF API
    path('cart/',  cart_html, name='cart'),
    path('products/', ProductListHTMLView.as_view(), name='products'),  # ✅ fixed
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


