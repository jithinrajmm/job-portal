# Generated by Django 4.0.6 on 2022-08-05 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_companies_spam'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_recruiter',
            field=models.BooleanField(default=False),
        ),
    ]
