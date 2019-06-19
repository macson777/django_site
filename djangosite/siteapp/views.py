from django.shortcuts import render, redirect
from siteapp.models import Category, Product
import telegram

# Create your views here.

def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'base.html', context)


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    context = {
        'category': category
    }
    return render(request, 'category.html', context)


def telegram_form(request):
    token = "759065563:AAHyNPXxXKLI7jn52uc55QWU2aQHLBWMXVE"
    chat_id = '-393705029'
    bot = telegram.Bot(token=token)
    if request.method == 'GET':
        return render(request, 'telegram_feedback_form.html')
    name = request.POST.get('user_name')
    phone_number = request.POST.get('user_phone')
    email = request.POST.get('user_email')
    message = request.POST.get('user_message')

    context = {
        'Имя пользователя:': name,
        'Телефон:': phone_number,
        'Email:': email,
        'Сообщение:': message,
    }

    text = ''
    for key, value in context.items():
        text += f'{key} {value}\n'

    bot.send_message(chat_id=chat_id, text=text)
    return redirect('http://127.0.0.1:8000')

