# Generated by Django 5.0 on 2024-02-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_usertoken_ua'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='avatar',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
