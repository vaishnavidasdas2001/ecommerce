from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=255,unique=True)


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255,null=True)
    price = models.IntegerField()
    discreption = models.CharField(max_length=255,null=True)
    pdt_image = models.ImageField(upload_to='images/', null=True)


class userDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    usr_image = models.ImageField(upload_to='images/',null=True)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    