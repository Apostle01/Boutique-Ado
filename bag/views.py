from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from products.models import Product #import the Product model

def view_bag(request):
    """A view that renders the bag contents page."""
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag."""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            # if 'items_by_size' not in bag[item_id]:
            #     # Initialize 'items_by_size' if it doesn't exist
            #     bag[item_id]['items_by_size'] = {}
            if size in bag[item_id]['items_by_size'].keys():
                # Correctly reference the size variable (not the string 'size')
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            # Create the item with size
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            # Increment the quantity if the item already exists
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # Add new item to the bag
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')

        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')

    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from products.models import Product  # Import the Product model

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        # Fetch the product object from the database
        product = get_object_or_404(Product, pk=item_id)

        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        
        bag = request.session.get('bag', {})

        if size:
            # Remove the item by size
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                # Remove the entire item if no sizes are left
                bag.pop(item_id)
        else:
            # Remove the item if there is no size
            bag.pop(item_id)

        # Update the session
        request.session['bag'] = bag

        # Success message indicating item removal
        messages.success(request, f'Removed {product.name} (size {size}) from your bag')

        return HttpResponse(status=200)

    except Exception as e:
        # Handle errors gracefully and return status 500
        print(f"Error: {e}")
        return HttpResponse(status=500)
