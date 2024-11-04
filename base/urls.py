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

    path("sub-category/", views.subCategorysView, name="sub-category"),
    path("sub-category/<int:pk>/", views.subCategoryView, name="single-sub-category"),
    path("create-sub-category/<int:pk>/", views.createSubCategoryView, name="create-sub-category"),

    path("products/", views.productsView, name="products"),
    path("product/<int:pk>/", views.productView, name="product"),
    path("create-product/<int:pk>/", views.createProductView, name="create-product"),
    path("edit-product/<int:pk>/", views.editProduct, name="edit-product"),

    path("carts/", views.cartsView, name="carts"),
    path("cart/<int:pk>/", views.cartView, name="cart-view"),
    path("delete-cart/<int:pk>/", views.deleteCartView, name="delete-cart"),

    path("orders/", views.orderView, name="orders"),
    path("orders/<int:pk>/", views.singleOrderView, name="order"),
    path("create-order/<int:pk>/", views.createOrderView, name="create-order"),
    path("delete-order/<int:pk>/", views.deleteOrderView, name="delete-order"),
]


