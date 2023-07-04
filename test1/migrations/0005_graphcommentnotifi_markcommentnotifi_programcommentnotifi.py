# Generated by Django 3.2.5 on 2021-11-03 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('graphdesign', '0002_auto_20210826_1224'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programming', '0002_auto_20210826_1224'),
        ('marketing', '0002_auto_20210826_1224'),
        ('test1', '0004_remove_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramCommentNotifi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stuff_name', models.TextField(default='Alaa', max_length=20)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_from_p', to=settings.AUTH_USER_MODEL)),
                ('prg_Comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='programming.progrmcomments')),
                ('prg_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pp', to='programming.progrmpost')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_to_p', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarkCommentNotifi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stuff_name', models.TextField(default='Alaa', max_length=20)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_from_m', to=settings.AUTH_USER_MODEL)),
                ('mrk_Comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mc', to='marketing.markcomments')),
                ('mrk_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mp', to='marketing.markpost')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_to_m', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GraphCommentNotifi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('stuff_name', models.TextField(default='Alaa', max_length=20)),
                ('user_has_seen', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_from_g', to=settings.AUTH_USER_MODEL)),
                ('gr_Comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gc', to='graphdesign.graphcomments')),
                ('gr_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gp', to='graphdesign.graphpost')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_to_g', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
