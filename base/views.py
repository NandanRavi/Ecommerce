from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .forms import CustomUserForm, CustomerForm, CartForm, CategoryForm, SubcategoryForm, ProductForm, OrderItemsForm
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser, Cart
from .utils import superuser_required
import re, urllib.parse, requests
# Create your views here.


# Home Page
def homePage(request):
    context = {}
    return render(request, "base/home.html", context)

# Customer Registration
def registerUser(request):
    form = CustomUserForm()
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.(com|in)$"
        form = CustomUserForm(request.POST)
        if not re.match(email_regex, email):
            messages.error(request, "Enter Correct Email!!!")
            return redirect("register")
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this email is already registered!!!")
        if password1 != password2:
            messages.error(request, "Both passwords should be the same!")
            return redirect("register")
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, "User created Successfully")
            return redirect("create-customer")
    else:
        form = CustomUserForm()
    context = {"form":form}
    return render(request, "base/customer/register.html", context)


# Customer Login
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email = request.POST['Email']
        password = request.POST['Password']

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, "Email doesn't exist")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully!!!")
            return redirect("customer")
        else:
            messages.error(request, 'Email or Password is incorrect')
    return render(request, "base/customer/login.html",)

# Login Google
def loginGoogleView(request):
    google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    client_id = settings.GOOGLE_CLIENT_ID
    state = urllib.parse.urlencode({'ip': request.META.get('REMOTE_ADDR', '')})
    auth_url = f"{google_auth_endpoint}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
    return redirect(auth_url)


# Oauth2callback
def oauth2callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code:
        messages.error(request, "Authorization code not provided.")
        return redirect("login")

    state_params = urllib.parse.parse_qs(state) if state else {}
    custom_data = state_params.get('ip', [None])[0]

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=data)
    token_data = token_response.json()

    if 'access_token' not in token_data:
        messages.error(request, "Failed to obtain access token from Google.")
        return redirect("login")

    access_token = token_data['access_token']

    userinfo_url = f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={access_token}"
    userinfo_response = requests.get(userinfo_url)
    userinfo = userinfo_response.json()

    email = userinfo.get('email')
    name = userinfo.get('name')

    if not email:
        messages.error(request, "Failed to retrieve user information from Google.")
        return redirect("login")

    user, created = CustomUser.objects.get_or_create(email=email, defaults={'name': name})

    if created:
        Customer.objects.create(user=user)
        messages.success(request, "User created successfully.")
    else:
        messages.success(request, "Login successful.")

    login(request, user)
    return redirect("customer" if created else "create-customer")


# Customer Logout
def logoutUser(request):
    logout(request)
    messages.error(request, "User was logged out!")
    return redirect('login')



# Customer View
@login_required(login_url="login")
def customerAccountView(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        messages.error(request, "No customer account found. Please complete your profile.")
        return redirect("customer")

    context = {"customer": customer}
    return render(request, "base/customer/customer.html", context)

# Customer Data Creation
@login_required(login_url="login")
def createCustomerView(request):
    user = request.user
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, "Customer Created Successfully")
            return redirect("customer")
    else:
        form = CustomerForm()
    context = {"form": form, "user":user}
    return render(request, "base/customer/create_customer.html", context)

# Edit Customer
@login_required(login_url="login")
def editCustomerAccountView(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Data Edited Successfully")
            return redirect("customer")
    else:
        form = CustomerForm(instance=customer)
    
    context = {"form": form, "customer": customer}
    return render(request, "base/customer/edit_customer.html", context)



# Category Related Functions Start
def categoryView(request):
    page = "category"
    categories = Category.objects.all()
    context = {"categories":categories, "page":page}
    return render(request, "base/category/category.html", context)

def singleCategoryView(request, pk):
    category = Category.objects.get(id=pk)
    subcategories = SubCategory.objects.filter(category=category)
    context = {"category":category, "subcategories":subcategories}
    return render(request, "base/category/single_category.html", context)

@superuser_required
def createCategoryView(request):
    page = "create_category"
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, "Category Created Successfully")
            return redirect("category")
    else:
        form = CategoryForm()
    context = {"form":form, "page":page}
    return render(request, "base/category/category.html", context)
# Category Related Function Ends


# Sub-Category Related Function Starts
def subCategorysView(request):
    page = "sub_category"
    categories = SubCategory.objects.all()
    context = {"categories":categories, "page":page}
    return render(request, "base/subcategory/sub_category.html", context)

def subCategoryView(request, pk):
    category = SubCategory.objects.get(id=pk)
    products = Product.objects.filter(category=category)
    context = {"category":category,"products":products}
    return render(request, "base/subcategory/single_sub_category.html", context)

@superuser_required
def createSubCategoryView(request, pk):
    page = "create_sub_category"
    category = Category.objects.get(id=pk)
    form = SubcategoryForm()
    if request.method == "POST":
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            messages.success(request, "Sub-Category Created Successfully")
            return redirect("category")
    else:
        form = SubcategoryForm()
    context = {"form":form, "category":category, "page":page}
    return render(request, "base/subcategory/sub_category.html", context)
# Sub-Category Related Function Ends



# Product Related Function Starts
def productsView(request):
    page = "all_products"
    products = Product.objects.all()
    context = {"products":products, "page":page}
    return render(request, "base/product/products.html", context)

def productView(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product":product}
    return render(request, "base/product/single_product.html", context)

@superuser_required
def createProductView(request, pk):
    page = "create_product"
    subcategory = SubCategory.objects.get(id=pk)
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = subcategory
            product.save()
            messages.success(request, "Product Created Successfully!!!")
            return redirect("products")
    else:
        form = ProductForm()
    context = {"form":form, "subcategory":subcategory, "page":page}
    return render(request, "base/product/products.html", context)


@superuser_required
def editProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("category")
    
    context = {"form": form, "product": product}
    return render(request, "base/product/edit_product.html", context)
# Product Related Function ends


# Cart Related Function starts
@login_required(login_url="login")
def cartsView(request):
    page = "all_carts"
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer, deleted_at=None)
    context = {"carts":carts, "page":page}
    return render(request, "base/cart/cart.html", context)

@login_required(login_url="login")
def cartView(request, pk):
    page = "single_cart"
    user = request.user
    customer = Customer.objects.get(user=user)
    cart = Cart.objects.get(customer=customer, id=pk, deleted_at=None)
    context = {"page":page, "cart":cart}
    return render(request, "base/cart/cart.html", context)


@login_required(login_url="login")
def createCartView(request, pk):
    page = "create_cart"
    user = request.user
    customer = Customer.objects.get(user=user)
    product = Product.objects.get(id=pk)

    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            cart_form = form.save(commit=False)
            cart_form.customer = customer
            cart_form.product = product
            cart_form.save()
            messages.success(request, "Cart is created successfully...")
            return redirect("carts")
    else:
        form = CartForm()

    context = {"user": user, "form": form, "product": product, "page": page}
    return render(request, "base/cart/create_update_cart.html", context)

@login_required(login_url="login")
def editCartView(request, pk):
    page="edit_cart"
    cart = Cart.objects.get(id=pk)
    form = CartForm(instance=cart)
    if request.method == "POST":
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect("carts")
    context = {"page":page, "form":form}
    return render(request, "base/cart/create_update_cart.html", context)


@login_required(login_url="login")
def deleteCartView(request, pk):
    cart = Cart.objects.get(id=pk)
    if request.method == "POST":
        try:
            cart.deleted_at = timezone.now()
            cart.save()
            messages.success(request, "Order Deleted Successfully!!!!")
            return redirect("orders")
        except Cart.DoesNotExist:
            messages.error(request, "Order DoesNotExist....")
            return redirect("orders")
    cart = Cart.objects.filter(id=pk).first()
    if not cart:
        messages.error(request, "Order does not exist.")
        return redirect("orders")
    context = {"object":id}
    return render(request, "delete.html", context)
# Cart Related Function ends



# Order Related Function Starts
@login_required(login_url="login")
def orderView(request):
    page = "totalOrders"
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.filter(customer=customer, deleted_at=None)
    context ={"user":user,"orders":orders, "page":page}
    return render(request, "base/order/order.html", context)

@login_required(login_url="login")
def singleOrderView(request, pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    order = Order.objects.get(customer=customer, id=pk, deleted_at=None)
    if order.deleted_at:
        messages.info(request, "Order is not Available")
        return redirect("orders")
    orderitem = OrderItems.objects.get(order=order)
    context = {"order":order, "user":user,"orderitem":orderitem}
    return render(request, "base/order/order.html", context)


@login_required(login_url="login")
def createOrderView(request, pk):
    custom_user = request.user
    user = Customer.objects.get(user=custom_user)
    product = Product.objects.get(id=pk)
    if product.stock == "Out-of-Stock":
        messages.warning(request, "Product is not available for order")
        return redirect("home")
    if request.method == "POST":
        form = OrderItemsForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(customer=user)
            if OrderItems.objects.filter(order=order).exists():
                messages.warning(request, "This product is already added to the order.")
            else:
                order_form = form.save(commit=False)
                order_form.order = order
                order_form.product = product
                order_form.save()
                messages.success(request, "Order is placed.....")
                return redirect("products")
    else:
        form = OrderItemsForm()
    context = {"form":form, "user":user, "product":product}
    return render(request, "base/order/create_order.html", context)


@login_required(login_url="login")
def deleteOrderView(request, pk):
    order = Order.objects.get(id=pk)
    id = order.order_id
    if request.method == "POST":
        try:
            order.deleted_at = timezone.now()
            order.save()
            messages.success(request, "Order Deleted Successfully!!!!")
            return redirect("orders")
        except Order.DoesNotExist:
            messages.error(request, "Order DoesNotExist....")
            return redirect("orders")
    order = Order.objects.filter(id=pk).first()
    if not order:
        messages.error(request, "Order does not exist.")
        return redirect("orders")
    context = {"object":id}
    return render(request, "delete.html", context)
# Order Related Function ends




