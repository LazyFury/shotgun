# Generated by Django 5.0 on 2024-02-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_post_description_alter_menu_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='enable_delete',
            field=models.BooleanField(default=False),
        ),
    ]
