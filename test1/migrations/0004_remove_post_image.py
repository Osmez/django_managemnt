# Generated by Django 3.2.4 on 2021-06-23 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0003_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
