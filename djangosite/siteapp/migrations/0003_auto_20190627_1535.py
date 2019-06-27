# Generated by Django 2.2.2 on 2019-06-27 12:35

from django.db import migrations, models
import django.db.models.deletion
import siteapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0002_auto_20190627_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10)),
                ('discount', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='siteapp.Category')),
            ],
            options={
                'verbose_name': 'POST',
                'verbose_name_plural': 'POSTS',
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'PRODUCT', 'verbose_name_plural': 'PRODUCTS'},
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=siteapp.models.images_folder)),
                ('is_main', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='siteapp.Post')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
    ]
