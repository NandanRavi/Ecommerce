from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Customer, Category, SubCategory, Product, OrderItems, Cart

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["contact_number","address"]

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

class SubcategoryForm(ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name"]

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "product_image", "price", "description", "quantity", "stock"]

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ["quantity"]

class OrderItemsForm(ModelForm):
    class Meta:
        model = OrderItems
        fields = ["quantity"]



