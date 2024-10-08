# Generated by Django 5.1 on 2024-09-03 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='field',
            new_name='field_of_work',
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='username',
            field=models.CharField(default='default@example.com', max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
