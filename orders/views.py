from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
from .forms import OrderCreateForm
from django.views.generic import ListView

# ------------------ DRF API Views ------------------

class ProductListView(generics.ListAPIView):
    queryset         = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset         = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListView(generics.ListAPIView):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCreateView(generics.CreateAPIView):
    queryset         = Order.objects.all()
    serializer_class = OrderSerializer

# ------------------ HTML Views ------------------

class ProductListHTMLView(ListView):
    model = Product
    template_name = 'orders/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        flavor = self.request.GET.get('flavor')
        if flavor:
            return Product.objects.filter(flavor=flavor)
        return Product.objects.all()

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'orders/product_detail.html', {'product': product})

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    qty  = int(request.POST.get('quantity', 1))
    cart[str(pk)] = cart.get(str(pk), 0) + qty
    request.session['cart'] = cart
    return redirect('cart')

def cart_html(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart_data.items():
        prod = get_object_or_404(Product, pk=int(pid))
        items.append({'product': prod, 'quantity': qty, 'total': prod.price * qty})
        total += prod.price * qty
    return render(request, 'orders/cart.html', {'cart': items, 'cart_total': total})

def order_create_html(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for pid, qty in request.session.get('cart', {}).items():
                OrderItem.objects.create(order=order, product_id=int(pid), quantity=qty)
            request.session['cart'] = {}
            return redirect('thank-you')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_form.html', {'form': form})

def thank_you(request):
    return render(request, 'orders/thank_you.html')

def redirect_to_products(request):
    return redirect('product-list')

