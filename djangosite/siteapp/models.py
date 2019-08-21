from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from uuslug import slugify
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
        slug = slugify(str(instance.name))
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

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    product_image = models.ImageField()

    def __str__(self):
        return f'Cart item for product {self.product.name}'

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        product_id = product.id
        product_images = ProductImage.objects.filter(product=product_id, is_active=True, is_main=True)
        for image in product_images:
            image = image.image
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price, product_image=image)
        if new_item not in cart.items.all():
            cart_products = []
            for cart_item in cart.items.all():
                cart_products.append(cart_item.product)
            if new_item.product not in cart_products:
                cart.items.add(new_item)
                cart.save()

    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def total_cart_price(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * float(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен'),
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey('Cart', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    # image = models.ImageField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'),
                                                           ('Доставка', 'Доставка')), default='Самовывоз')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return f'Заказ №{self.id}'
