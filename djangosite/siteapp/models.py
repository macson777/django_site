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


class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)
        
        
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def images_folder(instance, filename):
    filename = f'{instance.slug}.{filename.split(".")[1]}'
    return f'{instance.slug}/{filename}'


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    brand = models.ForeignKey('Brand', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=images_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


# class Client(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     phone = models.CharField(max_length=13)
#     message = models.CharField(max_length=500)
#


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Cart item for product {product.title}'

class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)