from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("register/", views.registerUser, name="register"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    
    path("customer/", views.customerAccountView, name="customer"),
    path("create-customer/", views.createCustomerView, name="create-customer"),
    path("edit-customer/", views.editCustomerAccountView, name="edit-customer"),
]


