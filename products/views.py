from django.shortcuts import render
from products.models import Product
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def product_list(request):
    # Retrieve all products
    products = Product.objects.all().order_by('id')

    # Implement search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filtering by category (ensure 'category__name' matches the actual model field)
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)  # Adjust 'category__name' if necessary

    # Sorting products
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = products.order_by(sort_by)

    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'category': category,
        'sort_by': sort_by,
        'query': query
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
