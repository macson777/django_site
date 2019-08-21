from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from siteapp.views import (
    base_view,
    menu_view,
    category_view,
    product_view,
    cart_view,
    add_to_cart_view,
    remove_from_cart_view,
    total_price,
    telegram_form,
    checkout_view,
    make_order_view,
    repeat_order_view,
	account_view,
	registration_view,
	login_view,
    homepage,
)

urlpatterns = [
    path('', base_view, name='base'),
    path('menu/', menu_view, name='menu'),
    path('category/<category_slug>/', category_view, name='category_detail'),
    path('product/<product_slug>/', product_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', make_order_view, name='make_order'),
    path('repeat_order/', repeat_order_view, name='repeat_order'),
    path('thank_you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('account/', account_view, name='account'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('base')), name='logout'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('total_price/', total_price, name='total_price'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('feedback/', telegram_form, name='telegram_form'),
    path('homepage/', homepage, name='homepage'),

]


