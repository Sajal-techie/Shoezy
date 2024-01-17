from django.urls import path

from . import views
urlpatterns = [
    path('view_products/', views.view_products, name='view_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_variant/<str:id>', views.add_variant, name='add_variant'),
    path('edit_product/<str:id>', views.edit_product, name='edit_product'),
    path('edit_variant/<str:id>', views.edit_variant, name='edit_variant'),
    path('delete_variant/<str:id>', views.delete_variant, name='delete_variant'),
    path('delete_product/<str:id>', views.delete_product, name='delete_product'),
    path('list_product/<str:id>', views.list_product, name='list_product'),
    path('search_product/', views.search_product, name='search_product'),
]
