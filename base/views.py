from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserForm, CustomerForm, CategoryForm, SubcategoryForm, ProductForm, OrderItemsForm
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Create your views here.


# Home Page
def homePage(request):
    context = {}
    return render(request, "base/home.html", context)

# Customer Registration
def registerUser(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            if CustomUser.objects.filter(email=email).exists():
                form.add_error("Email", "User already Exist")
            else:
                user = form.save(commit=False)
                user.save()
                login(request, user)
                messages.success(request, "User created Successfully")
                return redirect("create-customer")
        else:
            messages.success(request, "An error has occur during registration")
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
            return redirect("customer")
        else:
            messages.error(request, 'Email or Password is incorrect')
    return render(request, "base/customer/login.html",)

# Customer Logout
def logoutUser(request):
    logout(request)
    messages.error(request, "User was logged out!")
    return redirect('login')



# Customer View
@login_required(login_url="login")
def customerAccountView(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context = {"customer":customer}
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
            return redirect("customer")
    else:
        form = CustomerForm(instance=customer)
    
    context = {"form": form, "customer": customer}
    return render(request, "base/customer/edit_customer.html", context)


def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser, login_url='login')(function)

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


# Order Related Function ends
@login_required(login_url="login")
def orderView(request):
    page = "totalOrders"
    user = request.user
    orders = Order.objects.all()
    context ={"user":user,"orders":orders, "page":page}
    return render(request, "base/order/order.html", context)

@login_required(login_url="login")
def singleOrderView(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
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
    context = {}
    return render(request, "base/order/delete_order.html", context)
