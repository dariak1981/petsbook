# Generated by Django 3.0.4 on 2020-06-26 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_auto_20200627_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intro',
            name='content',
            field=models.TextField(blank=True, max_length=800, verbose_name='content eng'),
        ),
        migrations.AlterField(
            model_name='intro',
            name='content_ru',
            field=models.TextField(blank=True, max_length=800, verbose_name='content'),
        ),
    ]
