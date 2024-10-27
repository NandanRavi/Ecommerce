from django.db import models
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.product_id
    
    

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

    def __str__(self):
        return self.order.order_id
    
    
class PaymentDetails(models.Model):
    order_number = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=10, unique=True, editable=False)
    amount = models.IntegerField(editable=False)
    status = models.BooleanField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.payment_id = f"ORD{self.pk:05d}"
            self.save(update_fields=['payment_id'])
        else:
            super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.amount = sum(item.product.price * item.quantity for item in self.order_number.orderitems_set.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.order_number.order_id} is {self.amount}"
        # return self.payment_id
    

    





