# Generated by Django 3.0.4 on 2020-06-19 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('title_ru', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('is_featured', models.BooleanField(default=False)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=20000, verbose_name='content')),
                ('photo', models.ImageField(blank=True, upload_to='blog/%Y/%m/%d/', verbose_name='photo')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Themes', verbose_name='theme')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=1500, verbose_name='message')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ['-created'],
            },
        ),
    ]
