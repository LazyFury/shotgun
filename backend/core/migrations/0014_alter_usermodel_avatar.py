# Generated by Django 5.0 on 2024-02-01 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_usermodel_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='avatar',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to='static/uploads/'),
        ),
    ]
