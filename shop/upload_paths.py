def product_image_path(instance, filename):
    return f'products/{instance.stone.slug}/{filename}'