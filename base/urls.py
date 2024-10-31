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

    path("category/", views.categoryView, name="category"),
    path("category/<int:pk>/", views.singleCategoryView, name="single-category"),
    path("create-category/", views.createCategoryView, name="create-category"),

    path("sub-category/", views.subCategoryView, name="sub-category"),
    path("category/<int:pk>/add-subcategory/", views.createSubCategoryView, name="create-sub-category"),
]


