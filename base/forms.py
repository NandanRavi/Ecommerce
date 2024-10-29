from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Customer, Category, SubCategory, Product, OrderItems

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
        fields = ["sub_category"]

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "product_image", "price", "description"]


class OrderItemsForm(ModelForm):
    class Meta:
        model = OrderItems
        fields = ["quantity"]


