from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import OrderCreateForm
from .services import create_order_cart
from .tasks import send_order_confirmation_email, process_successful_payment

def create_order(request):
	cart = Cart(request)
	if not len(cart):
		return redirect("shop:product_list")

	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			try:
				order = create_order_cart(form, cart)
			except ValueError as e:
				messages.error(request, str(e))
			else:
				cart.clear()
				# СИМУЛЯЦИЯ ОПЛАТЫ
				order.paid = True
				order.save(update_fields=['paid'])

				send_order_confirmation_email.delay(order.id)
				process_successful_payment.delay(order.id)
				
				return render(request, "orders/created.html", {"order": order})
	else:
		form = OrderCreateForm()

	return render(request, "orders/create.html", {"cart": cart, "form": form})