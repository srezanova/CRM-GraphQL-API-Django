# Generated by Django 3.2.5 on 2021-07-24 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_alter_request_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
    ]