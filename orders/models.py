from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    flavor = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField()
    address         = models.CharField(max_length=250)
    created         = models.DateTimeField(auto_now_add=True)
    paid            = models.BooleanField(default=False)
    pickup_datetime = models.DateTimeField(null=True, blank=True)   # ← this line

    def __str__(self):
        return f"Order {self.id} by {self.first_name}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

