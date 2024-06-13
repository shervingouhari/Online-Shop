from django.shortcuts import render, get_object_or_404, get_list_or_404
from core.redis import Redis
from .models import Category, Product


def product_list(request, category_id=None, category_slug=None):
    categories = Category.objects.filter(products__available=True).distinct()
    if category_id and category_slug:
        current_category = get_object_or_404(
            Category,
            id=category_id,
            slug=category_slug
        )
        products = get_list_or_404(current_category.products, available=True)
    else:
        products = get_list_or_404(Product, available=True)
    context = {
        'categories': categories,
        'products': products,
        'current_category': current_category if 'current_category' in locals() else None,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id, product_slug):
    product = Redis.get_prod_or_404(
        id=product_id,
        slug=product_slug,
        available=True
    )
    rec_products = Redis.rec_products([product])
    context = {
        'product': product,
        'rec_products': rec_products
    }
    return render(request, 'product_detail.html', context)
