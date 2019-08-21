from django.contrib import admin

#  Register your models here.

from siteapp.models import Category, Brand, Product, Cart, CartItem, Order, ProductImage


def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')


make_payed.short_description = "Пометить как оплаченные"


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(CartItem)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductImageInline]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class ProductImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage


admin.site.register(ProductImage, ProductImageAdmin)


