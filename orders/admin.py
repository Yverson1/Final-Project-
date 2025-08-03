from django.contrib import admin
from .models import Product, Order, OrderItem
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured', 'flavor', 'stock', 'image_preview')
    list_filter = ('featured', 'flavor')
    search_fields = ('name', 'description', 'flavor')
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'price', 'flavor', 'stock')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Status', {
            'fields': ('featured',),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 150px; border-radius: 8px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_image',)

    def product_image(self, obj):
        if obj.product.image:
            return format_html('<img src="{}" style="height: 50px;" />', obj.product.image.url)
        return "No image"
    product_image.short_description = 'Product Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'pickup_datetime', 'paid_status', 'created')
    list_filter  = ('paid', 'pickup_datetime')
    inlines      = [OrderItemInline]
    actions      = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(paid=True)
        self.message_user(request, f"{updated} orders marked as paid.")
    mark_as_paid.short_description = "Mark selected orders as paid"

    def paid_status(self, obj):
        color = 'green' if obj.paid else 'red'
        return format_html('<strong style="color: {};">{}</strong>', color, 'Paid' if obj.paid else 'Unpaid')
    paid_status.short_description = 'Status'
