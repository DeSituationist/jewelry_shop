from django.contrib import admin
from .models import Stone, Product

# Register your models here.
@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stone', 'kind', 'price', 'stock', 'available']
    list_editable = ['price', 'stock', 'available']
    list_filter = ['stone', 'kind', 'available']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}