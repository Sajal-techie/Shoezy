from django.urls import path

from . import views
urlpatterns = [
    path('admorders/', views.admorders, name='admorders'),
    # path('add_product/', views.add_product, name='add_product'),
    path('update_status/<str:id>', views.update_status, name='update_status'),
    path('update_date/<str:id>', views.update_date, name='update_date'),
#     path('list_product/<str:id>', views.list_product, name='list_product'),
#     path('search_product/', views.search_product, name='search_product'),
]
