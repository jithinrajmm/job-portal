# Generated by Django 4.0.6 on 2022-08-15 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_companies_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companies',
            options={'ordering': ('-updated',)},
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('Applicant', 'APPLICANT'), ('recruiter', 'RECRUITER')], default='Applicant', max_length=100),
        ),
        migrations.AlterField(
            model_name='companies',
            name='recruiter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
