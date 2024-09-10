from django.shortcuts import render, redirect, reverse, HttpResponse
# from django.shortcuts import get_object_or_404
# from products.models import Product

def view_bag(request):
    """A view that renders the bag contents page."""
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag."""

    # product = get_object_or_404(Product, pk=item_id)
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
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # Create the item with size
            bag[item_id] = {'items_by_size': {size: quantity}}

    else:
        if item_id in list(bag.keys()):
            # Increment the quantity if the item already exists
            bag[item_id] += quantity
        else:
            # Add new item to the bag
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    bag = request.session.get('bag', {})

    size = request.POST.get('product_size')  # Get size if provided

    if item_id in bag:
        if size:
            # Check if 'items_by_size' exists before trying to remove
            if 'items_by_size' in bag[item_id] and size in bag[item_id]['items_by_size']:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item_id)
        else:
            # Remove entire item if no size is specified
            bag.pop(item_id, None)

        request.session['bag'] = bag
        return HttpResponse(status=200)
    
    # Return 404 if item is not found in the bag
    return HttpResponse(status=404)
