from django.urls import path

from . import views
urlpatterns = [
    path('view_products/', views.view_products, name='view_products'),
    path('add_product/', views.add_product, name='add_product'),
]
