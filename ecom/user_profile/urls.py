from django.urls import path

from . import views
urlpatterns = [
    path('add_address/', views.add_address, name='add_address' ),
    path('delete_address/<str:id>/', views.delete_address, name='delete_address' ),
    path('view_profile/', views.view_profile, name='view_profile' ),
    path('reset_password/', views.reset_password, name='reset_password' ),
    path('edit_profile/<str:id>/', views.edit_profile, name='edit_profile' ),
    path('track_order/<str:id>', views.track_order, name='track_order'),
    path('track_order/<str:id>', views.track_order, name='track_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('cancel_order/<str:id>', views.cancel_order, name='cancel_order'),
  
]
