from django.urls import path
from .views import Return_management
from . import views

urlpatterns = [
    path('admorders/', views.admorders, name='admorders'),
    path('admorderitems/<str:id>', views.admorderitems, name='admorderitems'),
    path('update_status/<str:id>', views.update_status, name='update_status'),
    path('update_date/<str:id>', views.update_date, name='update_date'),
    path('view_returns/',Return_management.as_view(), name='view_returns'),

]
