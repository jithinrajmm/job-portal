# Generated by Django 4.0.6 on 2022-08-06 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]