from django.urls import path

from . import views
urlpatterns = [
    path('admlogin/', views.admlogin, name='admlogin' ),
    path('admhome/', views.admhome, name='admhome'),
    path('admusers/', views.admusers, name='admusers'),
    path('block_user/<str:id>', views.block_user, name='block_user'),
    path('unblock_user/<str:id>', views.unblock_user, name='unblock_user'),
    path('user_search/', views.user_search, name='user_search'),
    
    path('admbanners/', views.admbanners, name='admbanners'),


]
