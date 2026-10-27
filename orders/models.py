from django.db import models
from shop.models import Product

class Order(models.Model):
	first_name = models.CharField("Имя", max_length=20)
	last_name = models.CharField("Фамилия", max_length=20)
	email = models.EmailField("Email")
	address = models.CharField("Адрес", max_length=100)
	postal_code = models.CharField("Индекс", max_length=20)
	city = models.CharField("Город", max_length=25)
	created = models.DateTimeField("Создан", auto_now_add=True)
	paid = models.BooleanField("Оплачен", default=False)
	receipt_pdf = models.FileField("PDF-чек", upload_to="receipts/", blank=True, null=True)

	class Meta:
		ordering = ["-created"]
		verbose_name = "Заказ"
		verbose_name_plural = "Заказы"
		indexes = [models.Index(fields=["-created"])]

	def __str__(self):
		return f"Заказ №{self.pk}"

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(
		Order, related_name="items", on_delete=models.CASCADE, verbose_name="Заказ"
	)
	product = models.ForeignKey(
		Product, related_name="order_items", on_delete=models.CASCADE,
		verbose_name="Товар",
	)
	price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField("Количество", default=1)

	class Meta:
		verbose_name = "Позиция заказа"
		verbose_name_plural = "Позиции заказа"

	def __str__(self):
		return f"{self.product} × {self.quantity}"

	def get_cost(self):
		return self.price * self.quantity