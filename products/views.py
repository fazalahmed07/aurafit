from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    category_slug = request.GET.get('category')

    if query:
        products = products.filter(name__icontains=query)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/list.html', {
        'products': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'page_obj': page_obj,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})