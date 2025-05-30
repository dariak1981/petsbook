# Generated by Django 3.0.4 on 2020-07-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0003_auto_20200702_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('title_ru', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('posts', models.ManyToManyField(blank=True, to='blog.Post')),
            ],
        ),
    ]
