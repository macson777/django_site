# Generated by Django 2.2.2 on 2019-08-01 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0003_auto_20190801_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='item_image',
        ),
    ]
