from django import template

register = template.Library()

@register.filter
def cart_total_price(cart_items):
    return sum(item.product.price * item.quantity for item in cart_items)