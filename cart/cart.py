import copy
from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        current_amount = self.cart.get(product_id, {}).get('quantity', 0)
        wanted_amount = quantity if override_quantity else current_amount + quantity
        possible_amount = min(wanted_amount, product.stock)
        if possible_amount <= 0:
            self.remove(product)
            return True
        self.cart[product_id] = {'quantity': possible_amount, 'price': str(product.price)}
        self.save()
        return possible_amount < wanted_amount

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart: 
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        products = Product.objects.in_bulk([int(product_id)] for product_id in self.cart)
        for product_id, data in copy.deepcopy(self.cart).items:
            product = products.get(int(product_id))
            if product is None: continue
            data['product'] = product
            data['price'] = product.price
            data['total_price'] = product.price * data['quantity']
            yield data

    def  __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_sum(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()