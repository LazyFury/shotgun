# Generated by Django 5.0 on 2024-02-19 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_tablemanager_columns_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tablemanager',
            old_name='edit_form_fields',
            new_name='add_form_fields',
        ),
    ]
