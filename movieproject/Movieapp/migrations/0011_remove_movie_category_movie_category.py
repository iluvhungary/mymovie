# Generated by Django 4.2.9 on 2024-03-18 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movieapp', '0010_remove_movie_category_movie_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='category',
        ),
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.CharField(default='Default Category', max_length=100),
        ),
    ]
