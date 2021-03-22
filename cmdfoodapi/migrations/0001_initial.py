# Generated by Django 3.1.7 on 2021-03-22 23:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('zip_code', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(9999), django.core.validators.MaxValueValidator(100000)])),
                ('kroger_id', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kroger_id', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=19)),
                ('image_url', models.CharField(max_length=500)),
                ('aisle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Shopper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_img', models.ImageField(blank=True, upload_to='profiles/', verbose_name='Profile Image')),
                ('current_store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shoppers', related_query_name='shopper', to='cmdfoodapi.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productlists', related_query_name='productlist', to='cmdfoodapi.location')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productlists', related_query_name='productlist', to='cmdfoodapi.product')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productlists', related_query_name='productlist', to='cmdfoodapi.shopper')),
            ],
        ),
    ]
