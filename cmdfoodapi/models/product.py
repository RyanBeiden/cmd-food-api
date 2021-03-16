from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    kroger_id = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    image_url = models.ImageField(_("Product Image"), blank=True, upload_to='products/')
    aisle_number = models.IntegerField()
    aisle_side = models.CharField(max_length=2)
    aisle_bay = models.CharField(max_length=10)