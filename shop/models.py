from asyncio.windows_events import NULL
from email import message
import email
from email.policy import default
from enum import unique
from unicodedata import category, name
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.category


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.FloatField(default=0)
    desc = models.TextField(default="Description Here")
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user=  models.ForeignKey(User,
                                  on_delete=models.CASCADE, null= True, unique=False)
    name = models.CharField(max_length=150, null= False, default='')
    email = models.EmailField(null= False)
    phone= models.CharField(max_length=12, null= False, default= 1)
    address = models.TextField( null= False)
    city = models.CharField(max_length=100 , null= False)
    state = models.CharField(max_length=100 , null= False, default="USA")
    country = models.CharField(max_length=100, null= False) 
    zip_code = models.CharField(max_length=6, null= False)  
    total_price= models.FloatField(null= False)
    payment_mode= models.CharField(max_length=50, null= False)
    payment_id= models.CharField(max_length=150, null= True)
    orderstatus=(
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Completed', 'Completed')
    )
    status= models.CharField(max_length=50, choices= orderstatus, default='Pending')
    message=models.TextField(null= True,default= "Thanks For Ordering with us. We will update the status soon")
    tracking_no= models.CharField(max_length=150, null= True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id, self.tracking_no)

    

class OrderItem(models.Model):
        order = models.ForeignKey(Order,
                                  on_delete=models.CASCADE)
        product = models.ForeignKey(Product,
                                 on_delete=models.CASCADE)
        price = models.FloatField(null= False)
        quantity = models.PositiveIntegerField(default=1)

        def __str__(self):
            return '{} {}'.format(self.order.id, self.order.tracking_no)

        def get_cost(self):
            return self.price * self.quantity
        
        
class ContactForm(models.Model):
    user=  models.ForeignKey(User,
                                  on_delete=models.CASCADE, null= True, unique=False)
    name= models.CharField(max_length=150, null= False, default='')
    phone= models.CharField(max_length=12, null= False, default= 1)
    email= models.EmailField(null= False, default= '')
    subject= models.CharField(max_length=50, null= False, default='')
    message= models.CharField(max_length=1000, null= False, default='')
    
    def __str__(self):
        return self.name
        