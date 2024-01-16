from django.urls import path

from . import views
urlpatterns = [
    path('admorders/', views.admorders, name='admorders'),
    path('update_status/<str:id>', views.update_status, name='update_status'),
    path('update_date/<str:id>', views.update_date, name='update_date'),

]
