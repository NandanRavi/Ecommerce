from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserForm, CustomerForm, CategoryForm
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Create your views here.



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


def categoryView(request):
    page = "category"
    category = Category.objects.all()
    context = {"categories":category, "page":page}
    return render(request, "base/category.html", context)

def createCategoryView(request):
    page = "create-category"
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


def subCategoryView(request):
    context = {}
    return render(request, "base/sub_category.html", context)


def ProductView(request):
    context = {}
    return render(request, "base/products.html", context)


