# Generated by Django 5.0 on 2024-01-24 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_productskugroup_products_alter_product_skus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsku',
            name='old_price',
        ),
        migrations.RemoveField(
            model_name='productsku',
            name='price',
        ),
    ]
