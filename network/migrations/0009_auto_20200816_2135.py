# Generated by Django 3.0.8 on 2020-08-16 21:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20200805_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default=' Like ', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
