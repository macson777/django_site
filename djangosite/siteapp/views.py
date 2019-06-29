from django.shortcuts import render, redirect, HttpResponse
from siteapp.models import Category, Product, ProductImage, CartItem, Cart
import telegram
from .forms import FeedbackForm


# Create your views here.

def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    products = Product.objects.all()
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    context = {
        'products': products,
        'products_images': products_images,
        'cart': cart,
    }
    return render(request, 'base.html', context)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    product_images = ProductImage.objects.filter(slug=product_slug)
    context = {
        'product': product,
        'product_images': product_images,
        'cart': cart
    }

    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    context = {
        'category': category
    }
    return render(request, 'category.html', context)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
        return redirect('/cart/')


def remove_from_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    for cart_item in cart.items.all():
        if cart_item.product == product:
            cart.items.remove(cart_item)
            cart.save()
            return redirect('/cart/')


def telegram_form(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    token = "759065563:AAHyNPXxXKLI7jn52uc55QWU2aQHLBWMXVE"
    chat_id = '-393705029'
    bot = telegram.Bot(token=token)
    if request.method == 'GET':
        context = {'form': FeedbackForm(),
                   'cart': cart,
                   }
        return render(request, 'telegram_feedback_form.html', context)
    elif request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            message = data.get('message')

            context = {
                'Имя пользователя:': name,
                'Телефон:': phone,
                'Email:': email,
                'Сообщение:': message,
            }

            text = ''
            for key, value in context.items():
                text += f'{key}\n{value}\n'

            bot.send_message(chat_id=chat_id, text=text)
            return redirect('http://127.0.0.1:8000')
        else:
            errors = form.errors
            return HttpResponse(f'{errors}')
    return HttpResponse('Wrong request method')

