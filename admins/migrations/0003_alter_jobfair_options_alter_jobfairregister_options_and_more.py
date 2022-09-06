# Generated by Django 4.0.6 on 2022-08-17 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_jobfair_jobfairregister_jobfair_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobfair',
            options={'ordering': ('-conducted_date',)},
        ),
        migrations.AlterModelOptions(
            name='jobfairregister',
            options={'ordering': ('-registerd_date',)},
        ),
        migrations.AddField(
            model_name='jobfair',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]