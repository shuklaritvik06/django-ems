# Generated by Django 2.2.14 on 2023-06-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksmodel',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
    ]
