from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None  # Initialize categories to avoid UnboundLocalError

    if request.GET:
        if 'category' in request.GET:
            # Split category string into a list
            category_list = request.GET['category'].split(',')
            products = products.filter(category__name__in=category_list)
            categories = Category.objects.filter(name__in=category_list)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # Use double underscore for 'icontains' to perform a case-insensitive match
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # If no categories are filtered, set it to an empty list (to avoid None issues in the template)
    if categories is None:
        categories = []

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)  # Fix to use singular get_object_or_404

    context = {
        'product': product,
    }
    
    return render(request, 'products/product_details.html', context)
