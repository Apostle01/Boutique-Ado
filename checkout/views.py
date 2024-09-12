from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Py8shP86GD8AZmK2hvqdfhK2Br41mPOih7riU1mY2qQyn6oklWPEEcuDyitl8enkWJh9SgpdMPtcX9VV7mogg7D00drcK3okc',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
