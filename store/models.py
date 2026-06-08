from django.db import models
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    address=models.TextField()
    date=models.DateTimeField(default=datetime.datetime.now)
    status=models.CharField(max_length=100, default='Pending')

    def __str__(self):
        return self.product