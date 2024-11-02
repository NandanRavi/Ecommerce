from django.contrib import admin
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "name"]
    
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", "product__product_id"]

class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ["order_number", "payment_id", "amount", "status"]

admin.site.register(Customer)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
