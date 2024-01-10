# Generated by Django 5.0 on 2024-01-08 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0004_remove_qrcode_wx_alter_qrcode_type_delete_wxqrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='status',
            field=models.CharField(choices=[('normal', '正常'), ('deleted', '已删除')], default='normal', max_length=10),
        ),
    ]
