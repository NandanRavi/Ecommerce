from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserForm, CustomerForm, CategoryForm, SubcategoryForm, ProductForm
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
    return render(request, "base/register.html", context)


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
    return render(request, "base/login.html",)

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
    return render(request, "base/customer.html", context)

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
    return render(request, "base/create_customer.html", context)

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
    return render(request, "base/edit_customer.html", context)


def superuser_required(function):
    return user_passes_test(lambda u: u.is_superuser, login_url='login')(function)

# Category Related Functions Start
def categoryView(request):
    page = "category"
    category = Category.objects.all()
    context = {"categories":category, "page":page}
    return render(request, "base/category.html", context)

def singleCategoryView(request, pk):
    category_item = Category.objects.get(id=pk)
    subcategory_datas = SubCategory.objects.filter(category=category_item)
    context = {"category_item":category_item, "subcategory_list":subcategory_datas}
    return render(request, "base/single_category.html", context)

@superuser_required
def createCategoryView(request):
    page = "create_category"
    form = CategoryForm()
    if request.method == "GET":
        form = CategoryForm(request.GET)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect("category")
    else:
        form = CategoryForm()
    context = {"form":form, "page":page}
    return render(request, "base/category.html", context)
# Category Related Function Ends


# Sub-Category Related Function Starts
def subCategorysView(request):
    page = "sub_category"
    sub_categories = SubCategory.objects.all()
    context = {"sub_categories":sub_categories, "page":page}
    return render(request, "base/sub_category.html", context)

def subCategoryView(request, pk):
    category = SubCategory.objects.get(id=pk)
    products = Product.objects.filter(category=category)
    context = {"category":category,"products":products}
    return render(request, "base/category_product.html", context)

@superuser_required
def createSubCategoryView(request, pk):
    page = "create_sub_category"
    category = Category.objects.get(id=pk)
    form = SubcategoryForm()
    if request.method == "GET":
        form = SubcategoryForm(request.GET)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.category = category
            subcategory.save()
            return redirect("category")
    else:
        form = SubcategoryForm()
    context = {"form":form, "category":category, "page":page}
    return render(request, "base/sub_category.html", context)
# Sub-Category Related Function Ends



# Product Related Function Starts
def productsView(request):
    page = "all_products"
    products = Product.objects.all()
    context = {"products":products, "page":page}
    return render(request, "base/products.html", context)

def productView(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product":product}
    return render(request, "base/single_product.html", context)

@superuser_required
def createProductView(request, pk):
    page = "create_product"
    subcategory = SubCategory.objects.get(id=pk)
    form = ProductForm()
    if request.method == "GET":
        form = ProductForm(request.GET)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = subcategory
            product.save()
            return redirect("products")
    else:
        form = ProductForm()
    context = {"form":form, "subcategory":subcategory, "page":page}
    return render(request, "base/products.html", context)


# Product Related Function ends
