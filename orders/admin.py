from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "paid", "created"]
    list_filter = ["paid", "created"]
    list_editable = ["paid"]
    search_fields = ["first_name", "last_name", "email"]
    date_hierarchy = "created"
    inlines = [OrderItemInline]