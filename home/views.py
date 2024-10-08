from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

def products(request):
    # Add logic to retrieve and display products here
    return render(request, 'product.html')