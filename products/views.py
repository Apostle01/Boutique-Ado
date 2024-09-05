from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products(request):
    """ A view to show all_products, including sorting and search queries """

    products = Product.objects.all()

    context = {
    'products': products,
    }
    
    return render(request, 'products/products.html', context)

def product_details(request, product_id):
    """ A view to show individual product details """

    products = get_objects_or_404(Product, pk=product_id)

    context = {
    'product': products,
    }
    
    return render(request, 'products/product_details.html', context)