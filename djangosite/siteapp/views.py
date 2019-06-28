from django.shortcuts import render, redirect, HttpResponse
from siteapp.models import Category, Product, ProductImage
import telegram
from .forms import FeedbackForm


# Create your views here.

def base_view(request):
    products = Product.objects.all()
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    return render(request, 'base.html', locals())


def product_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product_images = ProductImage.objects.filter(slug=product_slug)

    return render(request, 'product.html', locals())


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
        context = {'form': FeedbackForm()}
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

