# Generated by Django 3.0.8 on 2020-07-30 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200730_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='sender',
        ),
        migrations.AddField(
            model_name='post',
            name='sent',
            field=models.ManyToManyField(related_name='post_sent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
