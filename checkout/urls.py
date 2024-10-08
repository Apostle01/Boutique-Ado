from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),  # The checkout view
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),  # Corrected typo in 'success'
    path('wh/', webhook, name='webhook'),
]
