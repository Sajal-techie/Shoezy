from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name='home'),
    path('login/', views.login ,name='login'),
    path('register/', views.register ,name='register'),
    path('verifyreg/', views.verifyreg ,name='verifyreg'),


]
