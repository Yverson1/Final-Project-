from django.contrib import admin
from .models import Product, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display   = ('name', 'price', 'featured')
    list_filter    = ('featured',)
    search_fields  = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'pickup_datetime', 'paid', 'created')
    list_filter  = ('paid', 'pickup_datetime')
    inlines      = [OrderItemInline]

