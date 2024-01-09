from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name='home'),
    path('login/', views.login ,name='login'),
    path('register/', views.register ,name='register'),
    path('verifyreg/<str:id>', views.verifyreg ,name='verifyreg'),
    path('resendotp/<str:id>', views.resendotp ,name='resendotp'),
    path('forget_pass/', views.forget_pass ,name='forget_pass'),
    path('reset_pass/<str:id>', views.reset_pass ,name='reset_pass'),
    path('page_not_found/', views.page_not_found ,name='page_not_found'),
    path('logout/', views.logout ,name='logout'),

]
