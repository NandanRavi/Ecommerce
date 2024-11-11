from django.urls import path
from . import views

urlpatterns = [
    path("", views.homePage, name="home"),
    path("register/", views.registerUser, name="register"),
    path('email-verification/<str:token>/', views.emailVerificationView, name='verify_email'),
    path("login/", views.loginUser, name="login"),
    path("google-login/", views.loginGoogleView, name="google-login"),
    path('oauth2callback', views.oauth2callback, name='oauth2callback'),
    path("logout/", views.logoutUser, name="logout"),

    path("customer/", views.customerAccountView, name="customer"),
    path("create-customer/", views.createCustomerView, name="create-customer"),
    path("edit-customer/", views.editCustomerAccountView, name="edit-customer"),

    path("categorys/", views.categoryView, name="category"),
    path("categorys/<int:pk>/", views.singleCategoryView, name="single-category"),
    path("create-category/", views.createCategoryView, name="create-category"),

    path("sub-categorys/", views.subCategorysView, name="sub-category"),
    path("sub-categorys/<int:pk>/", views.subCategoryView, name="single-sub-category"),
    path("create-sub-category/<int:pk>/", views.createSubCategoryView, name="create-sub-category"),

    path("products/", views.productsView, name="products"),
    path("products/<int:pk>/", views.productView, name="product"),
    path("create-product/<int:pk>/", views.createProductView, name="create-product"),
    path("edit-product/<int:pk>/", views.editProduct, name="edit-product"),

    path("carts/", views.cartsView, name="carts"),
    path("carts/<int:pk>/", views.cartView, name="cart-view"),
    path("create-cart/<int:pk>/", views.createCartView, name="create-cart"),
    path("edit-cart/<int:pk>/", views.editCartView, name="edit-cart"),
    path("delete-cart/<int:pk>/", views.deleteCartView, name="delete-cart"),

    path("orders/", views.orderView, name="orders"),
    path("orders/<int:pk>/", views.singleOrderView, name="order"),
    path("create-order/<int:pk>/", views.createOrderView, name="create-order"),
    path("delete-order/<int:pk>/", views.deleteOrderView, name="delete-order"),

    path("transactions/", views.transactionHistoryView, name="transactions"),
    path("transactions/<int:pk>/", views.transactionHistoryView, name="transaction"),
    path('payment/success/<str:payment_id>/', views.payment_success_view, name='payment_success'),

]


