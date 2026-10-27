from django.db import transaction
from django.db.models import F
from shop.models import Product
from .models import Order, OrderItem

@transaction.atomic
def create_order_cart(form, cart):
    items = list(cart)
    products = Product.objects.select_for_update().in_bulk(item['product'].id for item in items)
    order = form.save()
    for item in items:
        product = products[item['product'].id]
        OrderItem.objects.create(order=order, product=product, price=product.price, quantity=item['quantity'])
        Product.objects.filter(id=product.id).update(stock=F('stock') - item['quantity'])
    return order