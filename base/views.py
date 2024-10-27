from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Create your views here.



def homePage(request):
    context = {}
    return render(request, "base/home.html", context)

# Register View
@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def get(self, request):
        return JsonResponse({"message": "Get Method not allowed!!!"}, status=400)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return JsonResponse({"error": "Name, Email and Password are required"}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)


        user = CustomUser.objects.create_user(name=name, email=email, password=password)
        user.save()

        return JsonResponse({"message": "User registered successfully"}, status=201)
        
    
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def get(self, request):
        return JsonResponse({"message": "Get Method not allowed!!!"}, status=400)

    def post(self, request):
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            email = data.get("email")
            password = data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            print("Error during login attempt:", e)
            return JsonResponse({"error": "An error occurred during login"}, status=500)
        
@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def get(self, request):
        return JsonResponse({"message": "Get Method not allowed!!!"}, status=400)

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Please Login!!!"}, status=401)

            logout(request)
            return JsonResponse({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"message":e}, status=400)