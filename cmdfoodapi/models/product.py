from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image_url = models.ImageField(_("Product Image"), blank=True, upload_to='products/')
    aisle_number = models.IntegerField()
    aisle_side = models.CharField(max_length=2)
    aisle_bay = models.CharField(max_length=10)
    picked_up = models.BooleanField()