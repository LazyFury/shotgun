# Generated by Django 5.0 on 2024-02-19 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_rename_edit_form_fields_tablemanager_add_form_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='pid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
