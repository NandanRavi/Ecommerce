from django.contrib import admin
from .models import Customer, Product, Category, Order, OrderItems, SubCategory, PaymentDetails, CustomUser
# Register your models here.


class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "payment_id", "amount"]
    

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(SubCategory)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
