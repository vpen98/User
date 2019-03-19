# Generated by Django 2.1.7 on 2019-03-17 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org', models.CharField(blank=True, max_length=128, verbose_name='住址')),
                ('telephone', models.CharField(blank=True, max_length=50, verbose_name='手机号码')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'db_table': 'UserProfile',
            },
        ),
    ]
