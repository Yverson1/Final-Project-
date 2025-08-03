# ----------------------------------------------------------
# setup.ps1: Automated installer for The Fudge Kettle backend
# ----------------------------------------------------------
$ErrorActionPreference = 'Stop'

Write-Host "1) Creating virtual environment..."
python -m venv venv

Write-Host "2) Activating virtual environment..."
# Use the .bat file to avoid PowerShell policy issues
& .\venv\Scripts\activate.bat

Write-Host "3) Installing dependencies..."
@"
Django>=4.0
djangorestframework
channels
django-environ
"@ | Out-File -Encoding utf8 requirements.txt
pip install -r requirements.txt

Write-Host "4) Starting Django project and apps..."
django-admin startproject fudge_kettle .
python manage.py startapp orders

Write-Host "5) Creating notifications app folder..."
New-Item -ItemType Directory notifications -Force
New-Item -ItemType File notifications\__init__.py -Force

Write-Host "6) Patching settings.py..."
$settings = "fudge_kettle\settings.py"
Add-Content $settings @"
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS += [
    'rest_framework',
    'channels',
    'orders',
]

ASGI_APPLICATION = 'fudge_kettle.asgi.application'
CHANNEL_LAYERS = @{
    'default' = @{
        'BACKEND' = 'channels.layers.InMemoryChannelLayer'
    }
}
"@

Write-Host "7) Creating .env.example..."
@"
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
"@ | Out-File -Encoding utf8 .env.example

Write-Host "8) Scaffolding boilerplate code files..."

# orders/models.py
@"
from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY', 'Ready for Pickup'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_price = total
        self.save()
        return total

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
"@ | Out-File -Encoding utf8 orders\models.py

# orders/serializers.py
@"
from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'unit_price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','user','status','total_price','created_at','updated_at','items')
        read_only_fields = ('total_price','created_at','updated_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                unit_price=item.get('unit_price', item['product'].price)
            )
        order.calculate_total()
        return order
"@ | Out-File -Encoding utf8 orders\serializers.py

# orders/views.py
@"
from rest_framework import generics, permissions
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
"@ | Out-File -Encoding utf8 orders\views.py

# orders/urls.py
@"
from django.urls import path
from .views import ProductListView, ProductDetailView, OrderCreateView, OrderListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
]
"@ | Out-File -Encoding utf8 orders\urls.py

# notifications/consumers.py
@"
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.group_name = f'user_{user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def send_order_update(self, event):
        await self.send_json(event['data'])
"@ | Out-File -Encoding utf8 notifications\consumers.py

# notifications/routing.py
@"
from django.urls import re_path
from .consumers import OrderConsumer

websocket_urlpatterns = [
    re_path(r'ws/orders/$', OrderConsumer.as_asgi()),
]
"@ | Out-File -Encoding utf8 notifications\routing.py

Write-Host "All done! 🎉"
Write-Host 'Run python manage.py migrate then python manage.py runserver'

