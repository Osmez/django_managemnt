# Generated by Django 3.2.5 on 2022-05-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0002_auto_20210826_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='programming-pic')),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/programming/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='progrmpost',
            name='image',
            field=models.ManyToManyField(blank=True, to='programming.Image'),
        ),
    ]
