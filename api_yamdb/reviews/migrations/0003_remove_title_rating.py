# Generated by Django 3.2 on 2023-01-05 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_title_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
