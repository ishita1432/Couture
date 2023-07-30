from django.contrib import admin
from .models import Category,Product,Cart,Order,OrderItem,Profile,SubCategory,Wishlist
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)





