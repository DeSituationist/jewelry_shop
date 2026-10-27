from django.db import models
from django.urls import reverse
from .upload_paths import product_image_path

# Create your models here.
class Stone(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse('shop:product_list_by_stone', args=[self.slug])
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    stone = models.ForeignKey(Stone, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_path, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Type(models.TextChoices):
        RING = 'ring', 'Ring'
        EARRINGS = 'earrings', 'Earrings'
        NECKLACE = 'necklace', 'Necklace'
        BRACELET = 'bracelet', 'Bracelet'
        PENDANT = 'pendant', 'Pendant'

    type = models.CharField(max_length=20, choices=Type.choices, default=Type.RING)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])