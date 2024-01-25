from django.urls import path
from . import views

urlpatterns = [
    path("contact_us/", views.contact_us, name="contact_us"),
    path("about_us/", views.about_us, name="about_us"),
    path("terms/", views.terms, name="terms"),
    path("send_message/", views.send_message, name="send_message"),
]
