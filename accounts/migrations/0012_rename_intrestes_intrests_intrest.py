# Generated by Django 4.0.6 on 2022-08-25 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_userprofile_view_count_count_viewed_by_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intrests',
            old_name='intrestes',
            new_name='intrest',
        ),
    ]