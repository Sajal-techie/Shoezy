from django.urls import path

from . import views
urlpatterns = [
    path('shop/', views.shop, name='shop' ),
    path('singleproduct/<str:id>/', views.singleproduct, name='singleproduct'),
    # path('change_size/<str:id>/', views.change_size, name='change_size'),
    path('seachitems/', views.seachitems, name='seachitems'),
  
]
