from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views._logout, name="logout"),
    path("login", views._login, name="login"),
    path("register", views.register_view, name="register")
]