from django.urls import path
from .import views

urlpatterns = [
    path('kente/', views.kente, name='kente'),
]