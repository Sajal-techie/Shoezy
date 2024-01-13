from django.urls import path

from . import views
urlpatterns = [
    path('shop/', views.shop, name='shop' ),
    path('singleproduct/<str:id>/', views.singleproduct, name='singleproduct'),
    path('reset_filters/', views.reset_filters, name='reset_filters'),
  
]
