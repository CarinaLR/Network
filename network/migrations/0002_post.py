# Generated by Django 3.0.8 on 2020-07-28 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('sender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='post_sent', to=settings.AUTH_USER_MODEL)),
                ('username', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='all_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
