from django.contrib import admin

#  Register your models here.

from siteapp.models import Category, Brand, Product, Cart, CartItem

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)