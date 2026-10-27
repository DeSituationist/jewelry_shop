from django.contrib import admin
from .models import Stone, Product

# Register your models here.
@admin.register(Stone)
class StoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields=['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'stone', 'type', 'price', 'stock', 'is_available']
    list_editable = ['price', 'stock']
    list_filter = ['stone', 'type']
    list_select_related = ["stone"]
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(boolean=True, description="Доступен", ordering="stock")
    def is_available(self, obj):
        return obj.available