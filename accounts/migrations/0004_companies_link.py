# Generated by Django 4.0.6 on 2022-08-06 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_is_recruiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='link',
            field=models.URLField(null=True),
        ),
    ]