from io import BytesIO
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from weasyprint import HTML
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
	try:
		order = Order.objects.prefetch_related('items__product').get(id=order_id)
		html = render_to_string('orders/order_confirmation.html', {'order': order})

		send_mail(
			subject=f"Заказ №{order.id} оформлен — Gemma",
			message=strip_tags(html),
			from_email=settings.DEFAULT_FROM_EMAIL,
			recipient_list=[order.email],
			html_message=html,
			fail_silently=False,
		)
	except Order.DoesNotExist:
		pass

@shared_task
def process_successful_payment(order_id):
	try:
		order = Order.objects.prefetch_related('items__product').get(id=order_id)
	except Order.DoesNotExist:
		return 'Order not found'

	html = render_to_string("orders/receipt.html", {"order": order})
	pdf = BytesIO()
	
	HTML(string=html, base_url=settings.SITE_URL).write_pdf(pdf)
	pdf.seek(0)

	order.receipt_pdf.save(f'receipt_{order_id}.pdf', ContentFile(pdf.read()), save=True)

	html_email = render_to_string('orders/order_confirmation.html', {'order': order})
	email = EmailMessage(
		subject=f"Оплата по заказу №{order.id} получена — Gemma",
		body=html_email,
		from_email=settings.DEFAULT_FROM_EMAIL,
		to=[order.email],
	)
	email.content_subtype = 'html'

	if order.receipt_pdf:
		with order.receipt_pdf.open('rb') as f:
			email.attach(f"receipt_{order.id}.pdf", f.read(), "application/pdf")

	email.send()
	return f'Processed order {order_id}'