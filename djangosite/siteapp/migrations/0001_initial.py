# Generated by Django 2.2.2 on 2019-07-29 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import siteapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('price_is_active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='siteapp.Category')),
            ],
            options={
                'verbose_name': 'PRODUCT',
                'verbose_name_plural': 'PRODUCTS',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=siteapp.models.images_folder)),
                ('is_main', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='siteapp.Product')),
            ],
            options={
                'verbose_name': 'Image for PRODUCT',
                'verbose_name_plural': 'Images for PRODUCTS',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('buying_type', models.CharField(choices=[('Самовывоз', 'Самовывоз'), ('Доставка', 'Доставка')], default='Самовывоз', max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Принят в обработку', 'Принят в обработку'), ('Выполняется', 'Выполняется'), ('Оплачен', 'Оплачен')], default='Принят в обработку', max_length=100)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteapp.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('item_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteapp.Product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='siteapp.CartItem'),
        ),
    ]
