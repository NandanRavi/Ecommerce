from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserForm, CustomerForm
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Create your views here.



def homePage(request):
    context = {}
    return render(request, "base/home.html", context)


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
                return redirect("home")
        else:
            messages.success(request, "An error has occur during registration")
    context = {"form":form}
    return render(request, "base/register.html", context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        email = request.POST['Email']
        password = request.POST['Password']

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, "UserName doesn't exist")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, "base/login.html",)


def logoutUser(request):
    logout(request)
    messages.error(request, "User was logged out!")
    return redirect('login')