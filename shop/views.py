from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    TrigramWordSimilarity,
)
from django.db.models import Q
from .models import Product, Stone

# Create your views here.

TYPO_SIMILARITY = 0.6  


def product_search(request):
    query = (request.GET.get("query") or "").strip()[:100]
    products = Product.objects.none()

    if len(query) >= 2:
        vector = SearchVector("name", "description", config="russian")
        search_query = SearchQuery(query, config="russian", search_type="websearch")
        
        matched_stones = [
            key for key, label in Stone.Name.choices
            if query.lower() in label.lower()
        ]

        q = (
            Q(search=search_query)
            | Q(name__icontains=query)
            | Q(description__icontains=query)
        )
        if matched_stones:
            q |= Q(stone__name__in=matched_stones)

        products = (
            Product.objects.select_related("stone")
            .annotate(search=vector)
            .filter(q)
            .distinct()
            .order_by("name")
        )

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "shop/search.html",
        {"page_obj": page_obj, "query": query, "total": paginator.count},
    )

def product_list(request, stone_slug=None):
    stone = None
    stones = Stone.objects.all()
    products = Product.objects.filter(stock__gt=0)
    
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