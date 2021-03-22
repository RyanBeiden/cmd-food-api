from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    kroger_id = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image_url = models.CharField(max_length=500)
    aisle = models.CharField(max_length=100)