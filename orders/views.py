# orders/views.py

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models      import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
from .forms       import OrderCreateForm
from django.shortcuts import render

def cart_view(request):
    # Example: pulling a session‐based cart. Adapt to your actual logic.
    session_cart = request.session.get("cart", {})  
    # Convert your session data into a list of line‐items:
    cart_items = []
    for prod_id, qty in session_cart.items():
        product = Product.objects.get(pk=prod_id)
        total = product.price * qty
        cart_items.append({
            "product": product,
            "quantity": qty,
            "total": total,
        })

    return render(request, "cart.html", {
        "cart": cart_items
    })
# --------------- DRF API Views ---------------

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

# ------------- HTML “Shop” Views -------------

def product_list_html(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail_html(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

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
    return render(request, 'cart.html', {'cart': items, 'cart_total': total})

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
    return render(request, 'order_form.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')


