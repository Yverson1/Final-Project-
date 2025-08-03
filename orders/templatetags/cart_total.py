from django import template

register = template.Library()

@register.filter
def get_cart_total(cart_items):
    """
    Sums up the `total` from each item dict.
    """
    return sum(item["total"] for item in cart_items)

