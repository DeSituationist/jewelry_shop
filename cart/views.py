from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponseRedirect
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, stock__gt=0)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        changed = cart.add(product, cd["quantity"], cd["override"])
        if changed:
            messages.warning(
                request,
                f"Доступно только {product.stock} шт. товара «{product.name}». "
                f"Количество в корзине уменьшено.",
            )
        else:
            messages.success(request, f"«{product.name}» добавлен в корзину.")
    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER") or reverse("cart:cart_detail")
    )

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"«{product.name}» удалён из корзины.")
    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})