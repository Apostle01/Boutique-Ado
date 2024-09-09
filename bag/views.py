from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from products.models import Product

def view_bag(request):
    """A view that renders the bag contents page."""
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag."""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})

    if size:
        if item_id in bag:
            if 'items_by_size' not in bag[item_id]:
                # Initialize 'items_by_size' if it doesn't exist
                bag[item_id]['items_by_size'] = {}
            if size in bag[item_id]['items_by_size']:
                # Correctly reference the size variable (not the string 'size')
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # Create the item with size
            bag[item_id] = {'items_by_size': {size: quantity}}

    else:
        if item_id in bag:
            # Increment the quantity if the item already exists
            bag[item_id] += quantity
        else:
            # Add new item to the bag
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
