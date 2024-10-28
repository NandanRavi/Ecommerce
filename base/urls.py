from django.urls import path
from .views import homePage, registerUser, loginUser, logoutUser

urlpatterns = [
    path("", homePage, name="home"),
    path("register/", registerUser, name="register"),
    path("login/", loginUser, name="login"),
    path("logout/", logoutUser, name="logout"),
]


