# Generated by Django 5.0 on 2024-01-31 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_usertoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='browser',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usertoken',
            name='device',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usertoken',
            name='ip',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usertoken',
            name='is_mobile',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usertoken',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usertoken',
            name='platform',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]