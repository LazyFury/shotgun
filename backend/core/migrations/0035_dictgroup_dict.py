# Generated by Django 5.0 on 2024-02-26 02:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_menu_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictGroup',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('enable_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': '字典组',
                'verbose_name_plural': '字典组',
            },
        ),
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('enable_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('string', '字符串'), ('number', '数字'), ('boolean', '布尔'), ('json', 'json')], default='string', max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dictgroup')),
            ],
            options={
                'verbose_name': '字典',
                'verbose_name_plural': '字典',
            },
        ),
    ]
