from django.db import models
from django.urls import reverse
from .upload_paths import product_image_path


class Stone(models.Model):
    class Name(models.TextChoices):
        PEARL = "pearl", "Жемчуг"
        AMETHYST = "amethyst", "Аметист"
        CORAL = "coral", "Коралл"
        MALACHITE = "malachite", "Малахит"
        JADE = "jade", "Нефрит"
        RHODONITE = "rhodonite", "Родонит"
        CRYSTAL = "crystal", "Кристалл"
        TURQUOISE = "turquoise", "Бирюза"
        AGATE = "agate", "Агат"
        CARNELIAN = "carnelian", "Сердолик"
        AMBER = "amber", "Янтарь"
        DOLOMITE = "dolomite", "Доломит"
        TOURMALINE = "tourmaline", "Турмалин"
        ZOISITE = "zoisite", "Цоизит"
        JASPER = "jasper", "Яшма"
        CATS_EYE = "cats_eye", "Кошачий глаз"

    name = models.CharField(max_length=20, choices=Name.choices, verbose_name='Название')
    slug = models.SlugField(max_length=100, allow_unicode=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["name"]
        verbose_name = "Камень"
        verbose_name_plural = "Камни"
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse("shop:product_list_by_stone", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, allow_unicode=True, verbose_name="Слаг")
    stone = models.ForeignKey(
        Stone, related_name="products", on_delete=models.CASCADE,
        verbose_name="Камень",
    )
    image = models.ImageField(
        upload_to=product_image_path, blank=True, verbose_name="Изображение",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена, ₽",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="В наличии")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")

    class Type(models.TextChoices):
        RING = "ring", "Кольцо"
        EARRINGS = "earrings", "Серьги"
        NECKLACE = "necklace", "Колье"
        BRACELET = "bracelet", "Браслет"
        PENDANT = "pendant", "Подвеска"

    type = models.CharField(
        max_length=20, choices=Type.choices, default=Type.RING,
        verbose_name="Тип изделия",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

    @property
    def available(self): return self.stock > 0