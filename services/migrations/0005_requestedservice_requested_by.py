# Generated by Django 5.1 on 2024-09-10 18:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_requestedservice_requested_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedservice',
            name='requested_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='requested_services', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
