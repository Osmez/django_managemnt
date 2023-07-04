# Generated by Django 3.2.5 on 2021-08-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_toapprove'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('Specialization', models.CharField(max_length=30)),
                ('passowrd1', models.CharField(max_length=30)),
                ('passowrd2', models.CharField(max_length=30)),
                ('section', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Toapprove',
        ),
    ]
