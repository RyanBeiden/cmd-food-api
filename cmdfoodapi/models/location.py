from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zip_code = models.PositiveIntegerField(validators=[MinValueValidator(9999), MaxValueValidator(100000)])