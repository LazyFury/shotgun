# Generated by Django 5.0 on 2024-02-19 07:28

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_permission_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablemanager',
            name='columns',
            field=core.models.JSONField(blank=True, max_length=1000, null=True),
        ),
    ]
