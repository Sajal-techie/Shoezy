from django.urls import path

from . import views
urlpatterns = [
    path('shop/', views.shop, name='shop' ),
    path('singleproduct/', views.singleproduct, name='singleproduct'),
  
]
