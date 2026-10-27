def product_image_path(instance, filename):
    category_slug = getattr(instance.category, 'slug', None) or 'no_category'
    return f'products/{category_slug}/{filename}'