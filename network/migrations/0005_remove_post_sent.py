# Generated by Django 3.0.8 on 2020-07-30 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200730_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='sent',
        ),
    ]