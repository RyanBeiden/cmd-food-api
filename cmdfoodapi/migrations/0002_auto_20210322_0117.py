# Generated by Django 3.1.7 on 2021-03-22 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdfoodapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=500),
        ),
    ]