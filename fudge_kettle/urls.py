# fudge_kettle/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from orders import views


urlpatterns = [
    path('',       TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('shop/',  include('orders.shop_urls')),  # shop HTML
    path('api/',   include('orders.urls')),       # DRF API
    path('cart/', views.cart_view, name='cart'),  # this line adds the cart route
    path('admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


