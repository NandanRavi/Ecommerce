from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .manager import UserManager
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["id"]

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    contact_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.name
    

class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sub_category
    
    

class Product(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=10, unique=True, editable=False)
    product_name = models.CharField(max_length=30)
    product_image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.product_id = f"PID{self.pk:05d}"
            self.save(update_fields=['product_id'])
        else:
            super().save(*args, **kwargs)

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=10, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.order_id = f"ORD{self.pk:05d}"
            self.save(update_fields=['order_id'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id
    

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    
    
    
class PaymentDetails(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=10, unique=True, editable=False)
    amount = models.FloatField(editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.amount = sum(item.product.price * item.quantity for item in self.order_number.orderitems_set.all())
            super().save(*args, **kwargs)
            self.payment_id = f"TXN{self.pk:05d}"
            super().save(update_fields=['payment_id'])
        else:
            super().save(*args, **kwargs)
    

# class UserPayment(models.Model):
#     PAYMENT_STATUS_CHOICES = [
#         ('initiated', 'Initiated'),
#         ('processing', 'Processing'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#     ]
    
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     payment_details = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)
#     status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='initiated')
#     payment_date = models.DateTimeField(default=timezone.now)
#     amount_paid = models.FloatField()
#     description = models.TextField(null=True, blank=True)





