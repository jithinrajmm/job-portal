# Generated by Django 4.0.6 on 2022-08-25 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_count_updated'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Count',
            new_name='Counts',
        ),
    ]