from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views._logout, name="logout"),
    path("login", views._login, name="login"),
    path("register", views.register_view, name="register"),
    path("addmoney/<int:amount>", views.addmoney, name="addmoney"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("addaddress", views.addaddress, name="addaddress"),
    path("addinventory", views.addinventory, name="addinventory"),
    path("addproduct", views.addproduct, name="addproduct"),
    path("allproducts", views.allproducts, name="allproducts"),
    path("allproducts/<str:search>", views.allproducts, name="searchproducts")
]