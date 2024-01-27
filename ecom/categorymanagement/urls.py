from django.urls import path

from . import views

urlpatterns = [
    path("viewbrand/", views.viewbrand, name="viewbrand"),
    path("add_brand/", views.add_brand, name="add_brand"),
    path("edit_brand/<str:id>", views.edit_brand, name="edit_brand"),
    path("list_brand/<str:id>", views.list_brand, name="list_brand"), 
]
