from django.contrib import admin
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "product_name"]
    
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "product"]

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ["order_number", "payment_id", "amount"]

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
