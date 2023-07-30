from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    slug = models.SlugField(unique=True,null=False,blank=False)
    category_image = models.ImageField(upload_to='images/')
    description = models.TextField(max_length=2000,null=False,blank=False,default="") 
    status = models.BooleanField(default=False,help_text="0-default 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    slug = models.SlugField(unique=True,null=False,blank=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
       return self.name
   
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE,default="")
    slug = models.SlugField(unique=True,null=False,blank=False)
    product_name = models.CharField(max_length=150,null=False,blank=False)
    original_price = models.IntegerField(null=False,blank=False,default=0)
    selling_price = models.IntegerField(null=False,blank=False,default=0)
    product_description = models.TextField(max_length=2000,null=False,blank=False) 
    product_image = models.ImageField(upload_to='images/',default="")
    type = models.CharField(max_length=150,null=False,blank=False,default="")
    material = models.CharField(max_length=200,null=False,blank=False,default="")
    brand = models.CharField(max_length=150,null=False,blank=False,default="")
    trending = models.BooleanField(default=False,help_text="0-default 1-Hidden")
    status = models.BooleanField(default=False,help_text="0-default 1-Hidden")
    quantity = models.IntegerField(null=False,blank=False,default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
   
    def __str__(self):
       return self.product_name
   
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False,blank=False,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
       return self.product.product_name
   
    def get_total(self):
        return self.product.selling_price*self.product_quantity

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=150,null=False)
    lname = models.CharField(max_length=150,null=False)
    email = models.EmailField(max_length=150,null=False)
    phone = models.CharField(max_length=150,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode = models.CharField(max_length=150,null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    orderstatus = (
        ('Pending','Pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=150,choices=orderstatus,default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=250,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return '{}-{}'.format(self.id,self.tracking_no)
    
class OrderItem(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product  = models.ForeignKey(Product,on_delete=models.CASCADE,default="")
    price = models.FloatField(null=False,default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=False)
    
    def __str__(self) :
        return '{}-{}'.format(self.id,self.order.tracking_no)
    
    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        return total
    
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=150,null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode = models.CharField(max_length=150,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.user.username
    
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return self.product.product_name
   

    
    
    
    