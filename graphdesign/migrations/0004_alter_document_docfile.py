# Generated by Django 3.2.5 on 2022-05-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphdesign', '0003_graphpost_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/graphic/%Y/%m/%d'),
        ),
    ]
