from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from .models import Product, Stone

# Create your views here.
def product_search(request):
    ...

def product_list(request, stone_slug=None):
    stone = None
    stones = Stone.objects.all()
    products = Product.objects.filter(stock__gt=0, available=True)
    
    if stone_slug:
        stone = get_object_or_404(Stone, slug=stone_slug)
        products = products.filter(stone=stone)

    paginator = Paginator(products, 12)         
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'shop/list.html', {
        'stone': stone,
        'stones': stones,
        'page_obj': page_obj,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'shop/detail.html', {'product': product})