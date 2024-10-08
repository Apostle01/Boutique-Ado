from django.urls import path
from .import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>/', views.product_detail, name='product_detail'),
    # path('', views.product_list, name='product_list'),  # Example view for listing products
]
