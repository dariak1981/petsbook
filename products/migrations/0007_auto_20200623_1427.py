# Generated by Django 3.0.4 on 2020-06-23 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200622_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.CharField(max_length=20, verbose_name='price'),
        ),
    ]
