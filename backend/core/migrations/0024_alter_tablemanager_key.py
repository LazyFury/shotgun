# Generated by Django 5.0 on 2024-02-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_tablemanager_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablemanager',
            name='key',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]