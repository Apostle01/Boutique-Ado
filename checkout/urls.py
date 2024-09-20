from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),  # The checkout view
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),  # Corrected typo in 'success'
]
