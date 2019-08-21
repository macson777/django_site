from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from siteapp.models import Category, Product, ProductImage, CartItem, Cart, Order
from siteapp.forms import OrderForm, RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
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
    context = {
        'cart': cart,
    }
    return render(request, 'base.html', context)


def menu_view(request):
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
    return render(request, 'menu.html', context)


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
    product_id = product.id
    product_images = ProductImage.objects.filter(product=product_id)
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


def add_to_cart_view(request):
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
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(),
                         'cart_total_price': cart.cart_total,
                         })


def remove_from_cart_view(request):
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
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total': cart.items.count(),
                         'cart_total_price': cart.cart_total,
                         })


def total_price(request):
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
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart.total_cart_price(qty, item_id)
    cart_item = CartItem.objects.get(id=int(item_id))
    return JsonResponse({'cart_total': cart.items.count(),
                         'item_total': cart_item.item_total,
                         'cart_total_price': cart.cart_total,
                         })


def checkout_view(request):
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
    return render(request, 'checkout.html', context)


def make_order_view(request):
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
        context = {'form': OrderForm(),
                   'cart': cart,
                   }
        return render(request, 'order.html', context)
    elif request.method == 'POST':
        product_name = ''
        full_price = f'{cart.cart_total} BYN'
        i = 1
        for item in cart.items.all():
            product_name += f'------------------------------\n{i}. {item.product.name}\nколичество: {item.qty}\nцена: {item.item_total} BYN\n'
            i += 1
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            buying_type = data.get('buying_type')
            if buying_type == 'Доставка':
                address = data.get('address')
            else:
                address = '-'
            date = data.get('date')
            message = data.get('comments')
            # if message is True:
            #     message = '-'
            new_order = Order()
            new_order.user = request.user
            new_order.first_name = name
            new_order.items = cart
            new_order.total = cart.cart_total
            new_order.last_name = last_name
            new_order.phone = phone
            new_order.address = address
            new_order.buying_type = buying_type
            new_order.message = message
            new_order.save()
            context = {
                'Имя:': name,
                'Фамилия:': last_name,
                'Телефон:': phone,
                'Способ доставки:': buying_type,
                'Адрес: ': address,
                'Дата самовывоза/доставки:': date,
                'Сообщение:': message,
                'Товар:': product_name,
                'Итоговая сумма за заказ:': full_price,

            }

            text = f'З А К А З № {new_order.id}\n------------------------------\n'
            for key, value in context.items():
                text += f'\n{key}\n{value}\n'

            bot.send_message(chat_id=chat_id, text=text)
            del request.session['cart_id']
            del request.session['total']
            return redirect('thank_you')
        else:
            errors = form.errors
            return HttpResponse(f'{errors}')
    return HttpResponse('Wrong request method')


def repeat_order_view(request):
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
    token = "759065563:AAHyNPXxXKLI7jn52uc55QWU2aQHLBWMXVE"
    chat_id = '-393705029'
    bot = telegram.Bot(token=token)
    product_name = ''
    order_id = request.GET.get('order.id')
    print(order_id)
    order = Order.objects.get(id=order_id)
    i = 1
    for item in cart.items.all():
        product_name += f'------------------------------\n{i}. {item.product.name}\nколичество: {item.qty}\nцена: {item.item_total} BYN\n'
        i += 1

    new_order = Order()
    new_order.user = request.user
    new_order.first_name = order.first_name
    new_order.items = order.items
    new_order.first_name = order.first_name
    new_order.last_name = order.last_name
    new_order.phone = order.phone
    new_order.address = order.address
    new_order.buying_type = order.buying_type
    new_order.message = order.message
    new_order.total = order.total
    new_order.save()
    context = {
        'Имя:': order.first_name,
        'Фамилия:': order.last_name,
        'Телефон:': order.phone,
        'Способ доставки:': order.buying_type,
        'Адрес: ': order.address,
        'Дата самовывоза/доставки:': order.date,
        'Сообщение:': order.message,
        'Товар:': order.product_name,
        'Итоговая сумма за заказ:': order.full_price,

    }

    text = f'З А К А З № {new_order.id}\n------------------------------\n'
    for key, value in context.items():
        text += f'\n{key}\n{value}\n'

    bot.send_message(chat_id=chat_id, text=text)
    return redirect('thank_you')



def account_view(request):
        order = Order.objects.filter(user=request.user).order_by('-id')
        categories = Category.objects.all()
        context = {
            'order': order,
            'categories': categories
        }
        return render(request, 'account.html', context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return redirect('base')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return redirect('base')
    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'login.html', context)


def telegram_form(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=int(cart_id))
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


def order_form(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=int(cart_id))
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
        context = {'form': OrderForm(),
                   'cart': cart,
                   }
        return render(request, 'order.html', context)
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get('name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            address = data.get('address')
            buying_type = data.get('buying_type')
            date = data.get('date')
            message = data.get('message')

            context = {
                'Имя:': name,
                'Фамилия:': last_name,
                'Телефон:': phone,
                'Способ доставки:': buying_type,
                'Дата:': date,
                'Адрес:': address,
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


def homepage(request):
    return render(request, 'homepage.html')