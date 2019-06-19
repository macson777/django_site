from django.urls import path
from siteapp.views import base_view, category_view, product_view, telegram_form

urlpatterns = [
    path('', base_view, name='base'),
    path('category/<category_slug>/', category_view, name='category_detail'),
    path('product/<product_slug>/', product_view, name='product_detail'),
    path('feedback/', telegram_form, name='telegram_form'),
]


