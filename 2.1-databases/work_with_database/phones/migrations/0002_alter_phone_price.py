# Generated by Django 4.2 on 2023-05-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='price',
            field=models.FloatField(),
        ),
    ]
