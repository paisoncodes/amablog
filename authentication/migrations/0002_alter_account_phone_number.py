# Generated by Django 3.2.6 on 2021-08-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(help_text='Enter phone number with country code', max_length=14),
        ),
    ]