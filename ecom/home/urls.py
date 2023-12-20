from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name='home'),
    path('login/', views.login ,name='login'),
    path('register/', views.register ,name='register'),
    path('verifyreg/<str:id>', views.verifyreg ,name='verifyreg'),
    path('resendotp/<str:id>', views.resendotp ,name='resendotp'),

    path('logout/', views.logout ,name='logout'),



]
