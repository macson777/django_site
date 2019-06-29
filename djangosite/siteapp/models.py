from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


def images_folder(instance, filename):
    filename = f'{instance.slug}.{filename.split(".")[1]}'
    return f'{instance.slug}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    price_is_active = models.BooleanField(default=True)
    discount = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey('Category', blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

    def __str__(self):
        return str(self.price, self.name)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'PRODUCT'
        verbose_name_plural = 'PRODUCTS'


pre_save.connect(pre_save_category_slug, sender=Product)


class ProductImage(models.Model):
    product = models.ForeignKey('Product', blank=True, null=True, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=images_folder)
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Image for PRODUCT'
        verbose_name_plural = 'Images for PRODUCTS'


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Cart item for product {self.product.name}'


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)
