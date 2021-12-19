# Generated by Django 3.2.8 on 2021-12-19 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0007_auto_20211209_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.SmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
