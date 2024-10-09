from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='home'),
    # path('products/', views.products, name='products'),
    # path('profiles/', views.profiles_view, name='profiles'),
]
