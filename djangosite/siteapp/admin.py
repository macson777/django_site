from django.contrib import admin

#  Register your models here.

from siteapp.models import Category, Brand, Product, Cart, CartItem, ProductImage, PostImage, Post

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


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


class PostAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Post._meta.fields]
    inlines = [PostImageInline]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class PostImageAdmin (admin.ModelAdmin):
    list_display = [field.name for field in PostImage._meta.fields]

    class Meta:
        model = PostImage


admin.site.register(PostImage, PostImageAdmin)