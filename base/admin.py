from django.contrib import admin
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser, Cart
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "name"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "deleted_at"]

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "product__product_id", "deleted_at"]

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ["order_number", "payment_id", "amount", "status"]

class CartAdmin(admin.ModelAdmin):
    list_display = ["customer__user__id", "product__name", "quantity", "deleted_at"]

admin.site.register(Customer)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
admin.site.register(Cart, CartAdmin)
