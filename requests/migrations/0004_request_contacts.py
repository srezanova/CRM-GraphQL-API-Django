# Generated by Django 3.2.5 on 2021-07-23 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0003_auto_20210722_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='contacts',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]