from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderCreateForm
from .services import create_order_cart

# Create your views here.
def create_order(request):
    cart = Cart(request)
    if not len(cart): return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = create_order_cart(form, cart)
        cart.clear()
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})